load("@bazel_skylib//lib:unittest.bzl", "analysistest")

def _validation_outputs_test_impl(ctx):
  env = analysistest.begin(ctx)

  actions = analysistest.target_actions(env)
  target = analysistest.target_under_test(env)
  validation_outputs = target.output_groups._validation.to_list()
  for action in actions:
    for validation_output in validation_outputs:
      if validation_output in action.inputs.to_list():
        analysistest.fail(env,
            "%s is a validation action output, but is an input to action %s" % (
                validation_output, action))

  return analysistest.end(env)

validation_outputs_test = analysistest.make(_validation_outputs_test_impl)
