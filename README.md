# 🚨 InferSafe

**InferSafe** is a production-grade, self-healing LLM inference infrastructure inspired by companies like Together.ai. Built with modularity, resilience, and scalability in mind, it supports:

- ⚙️ Dynamic batching
- 🧠 Multi-model inference
- 📉 Token streaming
- 🔁 Failure detection and auto-recovery
- 📈 Prometheus metrics for observability
- 📈 Simulated autoscaling logic (based on concurrency & load)
- 🚀 Kubernetes-ready architecture

---

## 🔧 Architecture Overview

InferSafe is composed of:

- **FastAPI API Layer:** Entry point for all inference, reload, and metrics requests.
- **ModelWorker Instances:** Simulated LLMs (using TinyLLaMA or placeholders) with built-in retry and streaming.
- **MultiModelManager:** Handles GPU-aware routing and load balancing across multiple model workers.
- **Failure Detector:** Auto-heals failed models by reloading them and updating the worker pool.
- **Autoscaling Logic:** Monitors active request load and spins up/down worker instances based on thresholds (simulated).
- **Prometheus Metrics:** Exposes inference counts, latencies, retries, memory stats, and model health.

---

## 🧪 Features Implemented

| Feature                          | Status |
|----------------------------------|--------|
| Dynamic Batching & Inference     | ✅     |
| Token Streaming via Server-Sent Events | ✅ |
| Model Hot Reloading             | ✅     |
| Multi-Model Load Balancing       | ✅     |
| Simulated GPU-Aware Scheduling   | ✅     |
| Failure Detection & Recovery     | ✅     |
| Prometheus Observability         | ✅     |
| Dockerized Environment           | ✅     |
| Kubernetes YAML (basic setup)    | ✅     |
| Horizontal Autoscaling (Simulated) | ✅   |

---

## 📷 Screenshots (Swagger UI)

> Demonstrating working endpoints:

![Screenshot from 2025-06-18 22-44-21](https://github.com/user-attachments/assets/28ba9c25-8767-4a4d-a78e-41c3f775d6c4)

- `/generate-batch`: Returns a generated response from the model.

![Screenshot from 2025-06-18 22-45-17](https://github.com/user-attachments/assets/ba337b03-71bf-4a0c-a436-b488d0299ce4)
![Screenshot from 2025-06-18 22-46-01](https://github.com/user-attachments/assets/9234d56c-8005-469d-b992-d03e2048abd0)


- `/reload-model`: Dynamically reloads the model on failure.
![Screenshot from 2025-06-18 22-47-58](https://github.com/user-attachments/assets/1ee0a39d-8f31-41af-a26f-6d583409f9bf)

- `/metrics`: Exposes Prometheus-compatible metrics.
![Screenshot from 2025-06-18 22-46-44](https://github.com/user-attachments/assets/594c1ea6-5ba6-4bc9-8993-acfd7a0dd570)
![Screenshot from 2025-06-18 22-46-48](https://github.com/user-attachments/assets/68363aec-663e-499d-9294-d4b7ad709344)


## ⚙️ Simulated Autoscaling Logic

InferSafe simulates real-world autoscaling with:

- **Concurrency-aware scaling:** Spins up additional model workers when concurrent requests exceed a threshold.
- **Failure-aware fallback:** Automatically replaces failed workers and rebalances traffic.
- **Metrics-integrated decisions:** All scaling decisions are observable via Prometheus metrics (`active_workers`, `queued_requests`, etc.)

Although constrained by local resources, this logic mimics production Horizontal Pod Autoscalers (HPA) in Kubernetes.

---

## 📦 Running the Project

### 1. Clone and Build the Docker Image

```bash
git clone https://github.com/yourusername/InferSafe.git
cd InferSafe
docker build -t infersafe .
````

### 2. Run the Container

```bash
docker run -p 8000:8000 infersafe
```

### 3. Visit Swagger Docs

Open your browser at `http://localhost:8000/docs`

---

## ⚠️ Design Note on System Constraints

> This project was developed under limited local hardware constraints (8GB RAM, 4GB GPU), which restricted the use of large-scale LLMs or multi-GPU setups. And in load_test file I've tried to simulate real world scenario by passing in 10 prompts all together!
>
> As a result, the system **simulates**:
>
> * Multi-model workers
> * GPU-aware load balancing
> * Autoscaling decisions
>
> However, the architecture is fully modular and can plug directly into:
>
> * Real LLMs like LLaMA2, Mistral, or Mixtral
> * Actual GPU monitoring tools (like NVIDIA SMI)
> * Kubernetes Horizontal Pod Autoscaler (HPA) for scaling in production

💡 The core infrastructure is ready for production and only one deployment config away.

---

## 🔮 Future Improvements

* ✅ Integrate actual LLMs via HuggingFace Transformers
* ⏩ Replace simulation with true GPU load metrics
* 📦 Add Redis or Kafka for async job queues
* 📡 Use HPA for true horizontal scaling on K8s
* 🌐 Add WebSocket support for real-time UI streaming

---

## 🧠 Why This Matters

InferSafe was built to showcase:

* Resilience engineering for AI systems
* MLOps principles applied to inference pipelines
* Autoscaling and recovery design under system constraints
* Real-world thinking in system design

---

## 📚 Tech Stack

* `Python`, `FastAPI`, `Uvicorn`
* `Prometheus`, `Docker`
* `Kubernetes (basic YAMLs)`
* `pytest` for unit and load tests

---

---

## 🧪 Running Tests

Some tests involving actual inference are skipped by default if the model file (`.gguf`) is missing.

To enable full testing:

1. Download the `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf` model from [llama.cpp models](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)  
2. Place it in the `models/` directory.

```bash
pytest tests/


## 👨‍💻 Author

**Hindol R. Choudhury @InferSafe**
*Built with ❤️ 

---

## 📝 License

MIT License

