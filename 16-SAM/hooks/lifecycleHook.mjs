// CodeDeploy lifecycle hook for a Lambda deployment (Lab 16.4.3).
//
// CodeDeploy invokes this function with a DeploymentId and a
// LifecycleEventHookExecutionId. The function runs its checks and MUST
// report Succeeded or Failed with PutLifecycleEventHookExecutionStatus.
// If it never reports, the deployment waits and fails after one hour.
//
// Node.js 22 runtime, AWS SDK for JavaScript v3 (included in the runtime).
// The old aws-sdk (v2) package is not in the Node.js 18+ runtimes.

import {
  CodeDeployClient,
  PutLifecycleEventHookExecutionStatusCommand,
} from '@aws-sdk/client-codedeploy';
import { LambdaClient, InvokeCommand } from '@aws-sdk/client-lambda';

const codedeploy = new CodeDeployClient({});
const lambda = new LambdaClient({});

// Invokes the new function version directly (not through the alias, which
// still points at the old version during PreTraffic) and checks the result.
//
// TODO(student): make this a real test of your function. Send an event that
// looks like the ones your function gets in production (sam local
// generate-event helps), and check the parts of the response that matter.
// For the PostTraffic hook, consider testing through the alias or the API
// instead.
async function validate(functionVersionArn) {
  const response = await lambda.send(
    new InvokeCommand({
      FunctionName: functionVersionArn,
      Payload: JSON.stringify({ httpMethod: 'GET', path: '/hello' }),
    }),
  );

  if (response.FunctionError) {
    console.error(`New version returned a function error: ${response.FunctionError}`);
    return false;
  }

  const result = JSON.parse(Buffer.from(response.Payload).toString('utf8'));
  console.log(`New version returned statusCode ${result.statusCode}`);
  return result.statusCode === 200;
}

export const handler = async (event) => {
  const { DeploymentId: deploymentId, LifecycleEventHookExecutionId: lifecycleEventHookExecutionId } = event;
  const functionVersionArn = process.env.NEW_VERSION;
  console.log(`Deployment ${deploymentId}: validating ${functionVersionArn}`);

  // Default to Failed so that an exception still gets reported instead of
  // leaving CodeDeploy waiting for an hour.
  let status = 'Failed';
  try {
    status = (await validate(functionVersionArn)) ? 'Succeeded' : 'Failed';
  } catch (err) {
    console.error('Validation threw an error', err);
  }

  await codedeploy.send(
    new PutLifecycleEventHookExecutionStatusCommand({
      deploymentId,
      lifecycleEventHookExecutionId,
      status, // 'Succeeded' or 'Failed'
    }),
  );

  console.log(`Reported ${status} to CodeDeploy`);
  return status;
};
