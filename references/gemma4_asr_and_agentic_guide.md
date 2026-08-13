# 🚀 Comprehensive Technical Guide: Gemma 4 Model Family, Native ASR, and Agentic Workflows

## 📌 1. Overview of the Gemma 4 Model Family

Google DeepMind's **Gemma 4** represents a major evolution in open-weights AI architectures. Unlike legacy text-only decoders, the Gemma 4 family is built from the ground up as a **natively multimodal and agentic foundational model series** under the **Apache 2.0 license**.

### Key Innovations in Gemma 4:
- **Native Audio & ASR**: The **E2B**, **E4B**, and **12B** models feature integrated native speech recognition, speech-to-text translation, and audio understanding **without requiring external speech encoders** (like Whisper).
- **Encoder-Free Architecture**: Projects text, image, video, and raw audio spectrograms directly into a single unified transformer backbone using **Per-Layer Embeddings (PLE)**.
- **Native Agentic Intelligence**: Built-in function calling, tool usage execution, multi-step planning, and enforced JSON structured generation.
- **Ultra-Efficient Edge Footprint**: Designed for high performance on consumer GPUs and mobile/edge devices via 4-bit quantization and Unsloth acceleration.

---

## 📐 2. Gemma 4 Model Family Lineup

| Model | Parameter Architecture | Primary Modalities | Target Hardware & Footprint | Primary Features |
| :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E2B** | Dense + PLE (*Effective 2B*) | **Text, Image, Video, Native Audio (ASR)** | Mobile, Edge, 8GB GPU | Ultra-lightweight, Native ASR, Agentic Function Calling |
| **Gemma 4 E4B** | Dense + PLE (*Effective 4B*) | **Text, Image, Video, Native Audio (ASR)** | Edge, 12GB GPU | Balanced edge intelligence, Fast ASR & Speech-to-Text |
| **Gemma 4 12B** | Unified Dense (Encoder-Free) | **Text, Image, Video, Native Audio (ASR)** | Workstations, 16GB+ VRAM | High-accuracy ASR, Complex Reasoning, Agentic Workflows |
| **Gemma 4 26B A4B**| Mixture-of-Experts (MoE) | Text, Image, Video | Server / Multi-GPU | High throughput MoE, Low-latency serving |
| **Gemma 4 31B** | High-Capacity Dense | Text, Image, Video | Cloud / Data Center | Maximum reasoning & coding capacity |

*Note: The **E** prefix in **E2B** stands for "Effective Parameters" using Per-Layer Embedding (PLE) compression.*

---

## 🎙️ 3. Gemma 4 E2B Native ASR Architecture & Dataset Schema

### A. Audio Input Specifications
- **Format**: WAV / FLAC / MP3
- **Sampling Rate**: **16,000 Hz (16 kHz), Mono, 16-bit PCM**
- **Duration**: Ideal sample length **3–30 seconds**.

### B. Standard Multimodal OpenAI-Style Chat Dataset Schema for ASR

For training or fine-tuning Gemma 4 E2B on speech recognition (such as Nepali ASR using `Devanagari_Characters_Speech` or `Common Voice`), format the dataset as follows:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "तपाईं एक कुशल एआई सहायक हुनुहुन्छ जसले दिइएको अडियोलाई शुद्ध नेपाली देवनागरी पाठमा रूपान्तरण गर्दछ।"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "audio",
          "audio": "data/audio_001.wav"
        },
        {
          "type": "text",
          "text": "कृपया यो नेपाली अडियो ट्रान्सक्राइब गर्नुहोस्।"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "नेपाल एक अति सुन्दर र बहुसांस्कृतिक देश हो।"
    }
  ],
  "source": "https://github.com/tsumansapkota/Devanagari_Characters_Speech",
  "metadata": {
    "source": "Devanagari_Characters_Speech",
    "language": "ne",
    "task": "automatic_speech_recognition",
    "sampling_rate": 16000,
    "duration_seconds": 4.2
  }
}
```

---

## 🛠️ 4. Fine-Tuning Strategy for Gemma 4 E2B ASR (PyTorch + Unsloth)

Gemma 4 E2B can be fine-tuned efficiently on a single consumer GPU (e.g. 8GB VRAM RTX 3060/T4 or 16GB RTX 4090) using **QLoRA (4-bit quantization)**.

### Implementation Script (`train_gemma4_e2b_asr.py`):

```python
import torch
from datasets import load_dataset, Audio
from peft import LoraConfig, get_peft_model
from transformers import AutoProcessor, AutoModelForCausalLM, TrainingArguments
from trl import SFTTrainer

# 1. Load Model & Processor
MODEL_ID = "google/gemma-4-E2B-it"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    load_in_4bit=True,
    device_map="auto"
)

# 2. Configure LoRA specifically targeting Audio Projection & LLM Attention
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
        "embed_audio"  # Targets native audio embedding layers
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)

# 3. Training Setup
training_args = TrainingArguments(
    output_dir="./gemma4_e2b_nepali_asr",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    num_train_epochs=3,
    bf16=True,
    save_strategy="epoch",
    optim="paged_adamw_8bit"
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    peft_config=peft_config
)

trainer.train()
```

---

## 🤖 5. Agentic & Tool-Calling Capabilities of Gemma 4 E2B

Gemma 4 E2B includes **built-in agentic tool-use capabilities**. It can accept function signatures and respond with tool execution calls or structured JSON.

### Example Agentic Function Calling Prompt & Response

#### User Input with Tool Definitions:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an agentic assistant with access to local tools."
    },
    {
      "role": "tools",
      "content": [
        {
          "name": "search_nepali_dictionary",
          "description": "Searches standard Devnagari dictionary for meanings and spellings",
          "parameters": {
            "type": "object",
            "properties": {
              "word": {"type": "string"}
            },
            "required": ["word"]
          }
        }
      ]
    },
    {
      "role": "user",
      "content": "कृपया 'लालीगुराँस' शब्दको अर्थ र विवरण खोज्नुहोस्।"
    }
  ]
}
```

#### Gemma 4 Agentic Output (Tool Call):
```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "name": "search_nepali_dictionary",
      "arguments": {
        "word": "लालीगुराँस"
      }
    }
  ]
}
```

---

## 📑 6. Summary Checklist for Gemma 4 ASR & Agentic Workflow

1. **Model Selection**: Use **Gemma 4 E2B** or **Gemma 4 E4B** for native audio/ASR and agentic workflows on local hardware.
2. **Native Audio Processing**: No separate Whisper encoder needed—audio tokens project directly into Gemma 4's multimodal backbone.
3. **Dataset Format**: Maintain standard 16kHz mono audio with OpenAI `messages` containing `type: audio` and `type: text` content objects.
4. **Efficiency**: Train with QLoRA on 8GB-12GB VRAM GPUs using `Unsloth` or `peft`.
