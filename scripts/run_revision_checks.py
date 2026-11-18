"""Run the complete source, corpus and browser-model checks with fail-fast exit."""
from pathlib import Path
import subprocess,sys,shutil,json
R=Path(__file__).resolve().parents[1]
SITE=R.parent if R.name=='research' else R/'tmp/pathways-release'
node=shutil.which('node')
assert node,'Node.js is required for the portal checks'
subprocess.run([sys.executable,str(R/'scripts/build_source_review_coverage.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_source_economy_data.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_source_image_reviews.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_scoped_html_research.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_docx_source_review.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_inquiry_workbook.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_slo_learning_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_representation_information.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_euclid_area_extensions.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_polya_problem_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_polya_auxiliary_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_polya_definition_induction_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_polya_complete_copy_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_polya_part_iv_derivations.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_fraction_guide_reading_conditions.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_review_selection_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_heath_analysis_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_anderson_displayed_counts.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_dbr_measurement_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_brown_recording_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_palincsar_measurement_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/check_xin_problem_and_sample_models.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/literature_review.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/units_coordination_evidence.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_units_coordination_evidence.py')],cwd=R,check=True)
for script in ['test_advanced_math_models.py','test_general_math_models.py','test_curriculum_structure.py','test_content_completion.py','test_hierarchy_review.py','test_goal_hierarchy.py','test_content_objects.py','test_portal_retention.py','check_advanced_examples.py','check_applied_examples.py','check_early_number_goals.py','check_early_shape_measure_data_goals.py','check_primary_number_patterns.py','check_primary_geometry_measure_data.py','check_upper_primary_number_ratio.py','check_upper_primary_geometry_data.py','check_middle_number_algebra.py','check_middle_functions_statistics.py','check_middle_geometry.py','check_common_basic_one.py','check_common_basic_two.py','check_algebra_calculus_one.py','check_calculus_two_geometry.py','check_probability_statistics.py','check_economy_ai.py','check_work_culture_inquiry.py','audit_revision_quality.py','build_portal_data.py','build_relation_review_queue.py','test_curriculum_activities.py','audit_goal_network.py','write_hierarchy_transition_tables.py','validate_project.py','validate_authored_hierarchy.py']:
 subprocess.run([sys.executable,str(R/'scripts'/script)],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_literature_review.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_relation_analysis_reviews.py')],cwd=R,check=True)
subprocess.run([sys.executable,str(R/'scripts/test_ies_fractions_review.py')],cwd=R,check=True)
subprocess.run([node,str(R/'scripts/version_portal_assets.mjs')],cwd=R,check=True)
# Browser checks compare generated content with the bundled editable sources.
# Await this copy before testing; otherwise an authored revision can be compared
# with the preceding local research snapshot.
if R.name!='research':
 subprocess.run([sys.executable,str(R/'scripts/sync_research_source.py')],cwd=R,check=True)
for p in [SITE/'dist/app.js',SITE/'dist/hierarchy.js',*(SITE/'dist/modules').glob('*.mjs')]:
 subprocess.run([node,'--check',str(p)],cwd=SITE,check=True)
subprocess.run([node,str(R/'scripts/test_distribution_lab.mjs'),str(SITE/'dist')],cwd=R,check=True)
for script in ['test_network_model.mjs','test_pathways.mjs','test_flow_network.mjs','test_concept_flows.mjs','test_all_concept_pathways.mjs','test_school_revision.mjs','test_hierarchy_graph.mjs','test_catalog_groups.mjs','test_task_pathways.mjs','test_goal_network.mjs','test_content_objects.mjs']:
 subprocess.run([node,str(SITE/'tests'/script)],cwd=SITE,check=True)
catalog=json.loads((SITE/'dist/content/catalog.json').read_text(encoding='utf-8'))
(R/'data/revision_checks.json').write_text(json.dumps({'status':'pass','version':catalog['version'],'standards':435,'checks':['authored coverage and required fields','source provenance and references','JavaScript syntax','network model','task pathways and full AND groups','concept flow network','concept classification and search','all concept pathways','strict school scopes and 12-section corpus']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if R.name!='research':
 subprocess.run([sys.executable,str(R/'scripts/sync_research_source.py')],cwd=R,check=True)
print('All revision checks passed')
