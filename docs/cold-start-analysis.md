# Cold-Start Analysis

## What Is A Cold Start?

A cold start happens when the system needs to create new GPU capacity before it can serve more requests.

For a normal web application, scaling can be fairly quick.

For an LLM inference system, scaling is slower because the model server must wait for a GPU machine, start the container, load the model into GPU memory, and become ready to serve requests.

## Why Cold Starts Matter

GPU instances are expensive, so we do not want them running all the time if traffic is low.

But if we scale down too aggressively, the next traffic spike may suffer because new GPU capacity takes time to become ready.

So we need to measure the tradeoff:

- Scaling down saves money.
- Keeping capacity warm improves latency.
- Starting new GPU capacity creates delay.

## Cold-Start Timeline

| Stage | What Happens |
|---|---|
| Scale trigger | Autoscaling policy decides more capacity is needed |
| Pod pending | Kubernetes creates a new vLLM pod, but no GPU is available |
| Node provisioning | Karpenter asks AWS to create a GPU EC2 instance |
| Node ready | Kubernetes marks the new GPU node as ready |
| Pod scheduled | Kubernetes places the vLLM pod on the GPU node |
| Image pull | The vLLM container image is downloaded |
| Container start | The vLLM server starts running |
| Model load | The LLM weights load into GPU memory |
| Warm-up | The inference server becomes ready |
| First successful inference | The new replica serves its first real request |

## Metrics To Measure

| Metric | Formula Or Meaning |
|---|---|
| Total cold-start time | Time from scale trigger to first successful inference |
| Node provisioning time | Time from scale trigger to node ready |
| Pod scheduling time | Time from pod pending to pod scheduled |
| Image pull time | Time spent downloading the container image |
| Model load time | Time spent loading model weights into GPU memory |
| Warm-up time | Time from container start to first successful inference |

## Why This Is Important For Interviews

A simple project might say:

We autoscale when traffic increases.

A stronger project says:

GPU autoscaling is useful, but it is not instant. I measured the full cold-start path and found how much time was spent on node provisioning, image pull, model loading, and warm-up.

That shows deeper cloud engineering understanding.

## Possible Mitigations

Cold starts can be reduced by:

- keeping one small amount of GPU capacity warm
- using smaller or quantized models
- pre-pulling container images
- using faster storage for model weights
- tuning Karpenter provisioning settings
- using scheduled warm-up before expected traffic spikes

## Key Takeaway

Autoscaling saves money, but cold starts affect latency.

This project does not hide that problem. It measures it and explains the tradeoff clearly.