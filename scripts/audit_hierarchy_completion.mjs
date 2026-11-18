/** Read-only structural audit; writes only data/hierarchy_completion_audit.json. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceFiles = {
  standards: 'data/standards.json',
  authoredCommonClaims: 'data/hierarchy_common_claims.json',
  authoredAdvancedClaims: 'data/hierarchy_advanced_claims.json',
  authoredAppliedClaims: 'data/hierarchy_applied_claims.json',
  reviewRegistry: 'data/hierarchy_review_registry.json',
  taxonomy: 'data/concept_taxonomy.json',
  relations: 'data/revised_relations.json',
  legacyRelations: 'data/relations.json',
  pilot: 'data/hierarchy_pilot.json',
  revisionCoverage: 'data/revision_coverage.json',
  deployment: 'data/school_revision_deployment.json',
  catalog: 'tmp/pathways-release/dist/content/catalog.json',
  portalRelations: 'tmp/pathways-release/dist/content/connections.json',
  pathwaysIndex: 'tmp/pathways-release/dist/content/concept-pathways-index.json',
  taskCoverage: 'data/task_pathway_coverage.json',
  taskIndex: 'tmp/pathways-release/dist/content/task-pathways-index.json',
  taskCases: 'data/task_route_cases.json',
  goalNetworkAudit: 'data/goal_network_audit.json',
  integrationReview: 'data/hierarchy_integration_review.json',
  conditionReviewTable: 'data/goal_condition_review_table.json',
  transitionTable: 'data/hierarchy_transition_table.json',
  ...Object.fromEntries(fs.readdirSync(path.join(root,'data')).filter(name=>/^goal_hierarchy_.*\.json$/.test(name)).map(name=>[name, 'data/'+name])),
};
const data = Object.fromEntries(Object.entries(sourceFiles).map(([key, filename]) =>
  [key, JSON.parse(fs.readFileSync(path.join(root, filename), 'utf8'))]));
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const tally = (items, key) => items.reduce((out, item) => {
  const value = typeof key === 'function' ? key(item) : item[key];
  out[value ?? 'missing'] = (out[value ?? 'missing'] ?? 0) + 1;
  return out;
}, {});
const unique = items => [...new Set(items)];
const standardId = code => `standard:${code}`;
const standardCode = id => id.startsWith('standard:') ? id.slice(9) : null;
const standards = data.standards.standards;
const byCode = new Map(standards.map(item => [item.code, item]));
const catalogByCode = new Map(data.catalog.standards.map(item => [item.code, item]));
const relations = data.relations.relations;
const standardRelations = relations.filter(item => standardCode(item.from) && standardCode(item.to));
const directional = standardRelations.filter(item =>
  ['generalizes', 'requires_for_task'].includes(item.type) && item.review_state !== 'candidate');
const taskRelations = relations.filter(item => item.type === 'requires_for_task');
const pilotMaps = data.pilot.maps;
const pilotClaims = pilotMaps.flatMap(item => item.claims);

assert.equal(byCode.size, standards.length, 'Duplicate standard codes');
assert.equal(new Set(relations.map(item => item.id)).size, relations.length, 'Duplicate relation IDs');
for (const item of standardRelations) {
  assert.ok(byCode.has(standardCode(item.from)) && byCode.has(standardCode(item.to)), item.id);
}
// The working source can be ahead of the last successful deployment.
assert.equal(data.catalog.version, data.pathwaysIndex.version);
assert.equal(data.portalRelations.version, data.pathwaysIndex.version);
assert.deepEqual(relations, data.portalRelations.relations, 'Authoritative and deployed-source relations differ');
assert.equal(data.pathwaysIndex.coverage.standards, standards.length);
assert.equal(data.pathwaysIndex.coverage.relations, standardRelations.length);
assert.equal(data.taxonomy.groups.length, data.pathwaysIndex.groups.length);
assert.equal(data.conditionReviewTable.summary.all_goal_condition_records, data.goalNetworkAudit.coverage.condition_kinds.goal);
assert.equal(data.conditionReviewTable.summary.matching_review_snapshots, data.conditionReviewTable.summary.all_goal_condition_records);
for (const key of ['needs_review','removed_review_snapshots','source_changes_since_review']) assert.deepEqual(data.conditionReviewTable.summary[key], []);

function cyclicComponents(edges) {
  const adjacency = new Map(standards.map(item => [item.code, []]));
  for (const edge of edges) adjacency.get(standardCode(edge.from)).push(standardCode(edge.to));
  let next = 0;
  const stack = [], position = new Map(), low = new Map(), active = new Set(), components = [];
  function visit(node) {
    position.set(node, next);
    low.set(node, next++);
    stack.push(node);
    active.add(node);
    for (const target of adjacency.get(node)) {
      if (!position.has(target)) {
        visit(target);
        low.set(node, Math.min(low.get(node), low.get(target)));
      } else if (active.has(target)) low.set(node, Math.min(low.get(node), position.get(target)));
    }
    if (low.get(node) === position.get(node)) {
      const component = [];
      let value;
      do {
        value = stack.pop();
        active.delete(value);
        component.push(value);
      } while (value !== node);
      if (component.length > 1 || adjacency.get(node).includes(node)) components.push(component.sort());
    }
  }
  for (const code of adjacency.keys()) if (!position.has(code)) visit(code);
  return {
    cyclic_component_count: components.length,
    node_count: components.reduce((sum, component) => sum + component.length, 0),
    largest_component: Math.max(0, ...components.map(component => component.length)),
    components,
  };
}

const standardEntries = standards.map(item => {
  const id = standardId(item.code);
  const incoming = directional.filter(edge => edge.to === id);
  const outgoing = directional.filter(edge => edge.from === id);
  const taskIncoming = taskRelations.filter(edge => edge.to === id);
  const taskOutgoing = taskRelations.filter(edge => edge.from === id);
  const pilotIds = pilotMaps.filter(map => map.standards.includes(item.code) ||
    map.nodes.some(node => node.standards.includes(item.code))).map(map => map.id);
  return {
    code: item.code,
    school_level: item.school_level,
    grade_band: item.grade_band,
    subject: item.subject,
    domain: item.domain,
    source_review_status: catalogByCode.get(item.code).sourceReview,
    primary_concept_ids: data.taxonomy.groups.filter(group => group.primary_codes.includes(item.code)).map(group => group.id),
    concept_ids: data.pathwaysIndex.groups.filter(group => group.member_codes.includes(item.code)).map(group => group.id),
    directional_incoming_records: incoming.length,
    directional_outgoing_records: outgoing.length,
    directional_incoming_ids: incoming.map(edge => edge.id),
    directional_outgoing_ids: outgoing.map(edge => edge.id),
    distinct_directional_predecessors: unique(incoming.map(edge => standardCode(edge.from))),
    distinct_directional_successors: unique(outgoing.map(edge => standardCode(edge.to))),
    task_condition_incoming_records: taskIncoming.length,
    task_condition_outgoing_records: taskOutgoing.length,
    task_condition_incoming_ids: taskIncoming.map(edge => edge.id),
    task_condition_outgoing_ids: taskOutgoing.map(edge => edge.id),
    standard_relation_incident_records: standardRelations.filter(edge => edge.from === id || edge.to === id).length,
    pilot_map_ids: pilotIds,
    no_directional_incidence: incoming.length + outgoing.length === 0,
    order_decision: data.reviewRegistry.standards[item.code]?.order_decision ?? null,
    goal_and_route_inventory: data.taskCoverage.entries.find(entry=>entry.code===item.code),
  };
});
const entryByCode = new Map(standardEntries.map(item => [item.code, item]));
assert.ok(standardEntries.every(item => item.primary_concept_ids.length === 1), 'Primary classification is not a partition');
const noDirection = standardEntries.filter(item => item.no_directional_incidence);
const noTaskIncoming = standardEntries.filter(item => item.task_condition_incoming_records === 0);
const groups = data.pathwaysIndex.groups.map(group => {
  const members = new Set(group.member_codes);
  const incident = directional.filter(edge => members.has(standardCode(edge.from)) || members.has(standardCode(edge.to)));
  const internal = directional.filter(edge => members.has(standardCode(edge.from)) && members.has(standardCode(edge.to)));
  const internalCodes = new Set(internal.flatMap(edge => [standardCode(edge.from), standardCode(edge.to)]));
  const missing = group.member_codes.filter(code => entryByCode.get(code).no_directional_incidence);
  assert.equal(group.expansions, incident.length, group.id);
  return {
    id: group.id,
    title: group.title,
    domain: group.domain,
    primary_standard_count: data.taxonomy.groups.find(item => item.id === group.id).primary_codes.length,
    member_standard_count: group.members,
    member_codes: group.member_codes,
    portal_hierarchy_status: group.hierarchy_status,
    directional_incident_record_count: incident.length,
    directional_internal_record_count: internal.length,
    members_with_internal_directional_incidence: internalCodes.size,
    no_directional_incidence_count: missing.length,
    no_directional_incidence_codes: missing,
    pilot_map_ids: group.pilot_maps,
    independently_reviewed_hierarchies: group.reviewed,
    scopes: group.by_scope,
  };
});
const pairRecords = new Map();
for (const edge of standardRelations) {
  const key = `${edge.from}|${edge.to}|${edge.type}`;
  pairRecords.set(key, [...(pairRecords.get(key) ?? []), edge.id]);
}
const duplicatePairs = [...pairRecords.entries()].filter(([, ids]) => ids.length > 1)
  .map(([key, ids]) => ({ from_to_type: key, record_ids: ids }));
const fieldCoverage = records => Object.fromEntries([
  'review_state', 'independent_review', 'student_validated', 'diagnostic',
  'prerequisite_group', 'review_history', 'source_ids',
].map(field => [field, records.filter(item => Object.hasOwn(item, field)).length]));
const pilotCoverage = pilotMaps.map(map => ({
  id: map.id,
  title: map.title,
  declared_standard_codes: map.standards,
  node_standard_codes: unique(map.nodes.flatMap(node => node.standards)),
  node_count: map.nodes.length,
  route_count: map.routes.length,
  claim_count: map.claims.length,
  claim_types: tally(map.claims, 'kind'),
  independently_reviewed_claims: map.claims.filter(claim => claim.independent_review === true).length,
  student_validated_claims: map.claims.filter(claim => claim.student_validated === true).length,
  condition_groups: Object.entries(tally(map.claims.filter(claim => claim.condition_group), 'condition_group'))
    .map(([id, claimCount]) => ({ id, claim_count: claimCount })),
}));

const generatedAt = new Date();
const result = {
  schema_version: 1,
  audit_date: new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(generatedAt),
  generated_at_utc: generatedAt.toISOString(),
  audit_kind: 'structural_inventory_only',
  interpretation: '구조와 기록 상태만 감사한다. 관계의 수학적 타당성, 필수 선수성, 교수 순서 또는 학습 효과를 검증한 결과가 아니다.',
  definitions: {
    analysis_review_state: 'review_state는 관계 자체 분석의 표기다. legacy_draft는 이전 초안의 개별 분석 범위가 이 필드에 기록되지 않아 명시한 상태이며 자동 검토 완료가 아니다. 별도 hierarchy_review_registry의 선수성·위계 검토 상태와 구별한다.',
    directional_record: '성취기준→성취기준 관계 중 type이 generalizes 또는 requires_for_task이며 review_state가 candidate가 아닌 기록. 현 포털의 meaning_expansion 표시 조건을 재현한다.',
    no_directional_incidence: '위 방향 기록의 출발점이나 도착점으로 한 번도 나타나지 않는 성취기준. 선수 지식이 없거나 가장 기초인 목표라는 뜻이 아니다.',
    task_condition_record: 'type=requires_for_task인 모든 기록. element→standard인 기존 7개도 포함한다. 대상 기준 전체의 보편적 선수 조건이라는 뜻은 아니다.',
    record_count: '관계 ID의 수이며 서로 다른 기준 쌍의 수와 다르다. 동일 양 끝과 유형을 갖는 기록도 조건과 근거가 다를 수 있어 삭제 대상으로 단정하지 않는다.',
    concept_count: '46개 주 개념군. 추가 소속 때문에 개념군별 기준수와 미접촉 기준수를 합하면 중복될 수 있다.',
    pilot_mapping: '시범 map의 standards 또는 node의 standards에 코드가 포함되는 매핑. 해당 기준의 모든 목표와 경로가 완성됐다는 뜻이 아니다.',
    scope_missing: '소속 기준이 있는 학교급 범위에서 직접 내부 방향 기록이 0인 개념군. 한 기준만 있는 범위의 0도 자동 오류로 보지 않는다.',
    source_review_status: '배포 소스 catalog의 전체 435개 sourceReview 필드를 집계한다. 방향 관계 미접촉 151개만을 대상으로 한 수치가 아니며 원문 대조 기록은 수학적 분석 검토와 별개이다.',
    cycles: '의미 연결을 포함한 전체 그래프의 순환은 오류로 보지 않는다. 순서를 주장하는 부분 그래프의 순환을 별도로 집계한다.',
  },
  source_version: data.pathwaysIndex.version,
  pathways_dataset_version: data.pathwaysIndex.datasetVersion,
  source_hashes: Object.fromEntries(Object.entries(sourceFiles).map(([key, filename]) => [key, {
    path: filename,
    sha256: sha256(fs.readFileSync(path.join(root, filename))),
  }])),
  checks: {
    source_and_portal_relations_identical: true,
    catalog_connections_pathways_versions_match: true,
    deployment_matches_working_source: data.deployment.data_version === data.pathwaysIndex.version && data.deployment.task_dataset_version === data.taskIndex.datasetVersion && data.deployment.concept_dataset_version === data.pathwaysIndex.datasetVersion,
    valid_relation_endpoints_and_unique_ids: true,
    one_primary_concept_per_standard: true,
    computed_group_expansions_match_index: true,
  },
  summary: {
    standards: standards.length,
    concepts: groups.length,
    task_pathway_inventory: Object.fromEntries(Object.entries(data.taskCoverage).filter(([key])=>key!=='entries')),
    goal_network_inventory: data.taskIndex.goalGraph ?? null,
    goal_condition_integration_review: data.conditionReviewTable.summary,
    standards_without_explicit_goal_decomposition: standards.length-data.taskCoverage.goal_decomposed_standards,
    standards_by_school_level: tally(standards, 'school_level'),
    catalog_source_review_statuses: tally(data.catalog.standards, 'sourceReview'),
    portal_concept_statuses: tally(groups, 'portal_hierarchy_status'),
    relation_records: relations.length,
    relation_types: tally(relations, 'type'),
    standard_relation_records: standardRelations.length,
    explicit_instructional_sequences_in_standard_relations: standardRelations.filter(item => item.type === 'instructional_sequence').length,
    standard_relation_types: tally(standardRelations, 'type'),
    standard_relation_records_by_school_transition: tally(standardRelations, item =>
      `${byCode.get(standardCode(item.from)).school_level}→${byCode.get(standardCode(item.to)).school_level}`),
    standard_relation_review_states: tally(standardRelations, 'review_state'),
    standard_relation_review_states_by_type: Object.fromEntries(unique(standardRelations.map(item => item.type))
      .map(type => [type, tally(standardRelations.filter(item => item.type === type), 'review_state')])),
    directional_records: directional.length,
    directional_records_by_school_transition: tally(directional, item =>
      `${byCode.get(standardCode(item.from)).school_level}→${byCode.get(standardCode(item.to)).school_level}`),
    standards_with_directional_incidence: standards.length - noDirection.length,
    standards_without_directional_incidence: noDirection.length,
    no_directional_incidence_with_scoped_unordered_decision: noDirection.filter(item=>item.order_decision).length,
    no_directional_incidence_without_decision: noDirection.filter(item=>!item.order_decision).length,
    no_directional_incidence_by_school_level: tally(noDirection, 'school_level'),
    no_directional_incidence_by_subject: tally(noDirection, 'subject'),
    standards_without_any_standard_relation: standardEntries.filter(item => !item.standard_relation_incident_records).length,
    task_condition_records: taskRelations.length,
    task_condition_target_standards: standards.length - noTaskIncoming.length,
    task_condition_target_standards_by_school_level: tally(standardEntries.filter(item => item.task_condition_incoming_records), 'school_level'),
    task_condition_records_with_structured_prerequisite_group: taskRelations.filter(item => item.prerequisite_group).length,
    prerequisite_group_operators: tally(taskRelations.filter(item => item.prerequisite_group), item => item.prerequisite_group.operator),
    independently_reviewed_concepts: data.pathwaysIndex.coverage.independently_reviewed_hierarchies,
    independently_reviewed_standard_relations: standardRelations.filter(item => item.independent_review === true).length,
    student_validated_standard_relations: standardRelations.filter(item => item.student_validated === true).length,
    independently_reviewed_standard_analyses: data.revisionCoverage.entries.filter(item => item.independentReview === true).length,
    student_validated_standard_analyses: data.revisionCoverage.entries.filter(item => item.studentValidated === true).length,
    pilot_maps: pilotMaps.length,
    pilot_nodes: pilotMaps.reduce((sum, item) => sum + item.nodes.length, 0),
    pilot_routes: pilotMaps.reduce((sum, item) => sum + item.routes.length, 0),
    pilot_claims: pilotClaims.length,
    pilot_claim_types: tally(pilotClaims, 'kind'),
    pilot_mapped_standards: standardEntries.filter(item => item.pilot_map_ids.length).length,
    standard_relation_field_presence: fieldCoverage(standardRelations),
    task_condition_field_presence: fieldCoverage(taskRelations),
    duplicate_from_to_type_groups: duplicatePairs.length,
    distinct_from_to_type_groups: pairRecords.size,
  },
  no_directional_incidence_codes: noDirection.map(item => item.code),
  no_task_condition_incoming_codes: noTaskIncoming.map(item => item.code),
  zero_direction_concept_ids: groups.filter(group => !group.directional_incident_record_count).map(group => group.id),
  nonempty_scopes_without_direction: groups.flatMap(group => Object.entries(group.scopes)
    .filter(([, scope]) => scope.members > 0 && !scope.expansions)
    .map(([scope, details]) => ({ concept_id: group.id, title: group.title, scope, members: details.members }))),
  cycles: {
    all_standard_relations: cyclicComponents(standardRelations),
    directional_relations: cyclicComponents(directional),
    task_condition_relations: cyclicComponents(standardRelations.filter(item => item.type === 'requires_for_task')),
    generalizes_relations: cyclicComponents(standardRelations.filter(item => item.type === 'generalizes')),
  },
  groups,
  standards: standardEntries,
  pilots: pilotCoverage,
  duplicate_from_to_type_records: duplicatePairs,
};
const output = path.join(root, 'data/hierarchy_completion_audit.json');
fs.writeFileSync(output, `${JSON.stringify(result, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ output: path.relative(root, output), source_version: result.source_version, summary: result.summary }, null, 2));
