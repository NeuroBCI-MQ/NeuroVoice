# NeuroVoice

A context-aware communication system for people who can't speak. NeuroVoice listens
to a conversation, uses a local LLM to propose likely replies, and lets the user
confirm one with simple yes / next / none signals — designed to be driven by EEG
(brain and muscle signals) as the input.

## How it works

1. **Listen:** the other person's speech is transcribed locally with Whisper
2. **Propose:** a local LLM (Llama 3.2 via Ollama) suggests short replies using the conversation history
3. **Select:** the user cycles through replies with three signals: yes / next / none of these
4. **Speak:** the chosen reply is spoken aloud
5. **Log:** every decision is saved to build personalization data

All processing runs on-device — no conversation data leaves the computer.

## Input modes

| Mode | Signal | Status |
|------|--------|--------|
| Keyboard | y / n / x keys | ✅ Working (development stand-in) |
| A: Artifacts | Eye blinks + jaw clenches (EEG) | Planned |
| B: Motor imagery | Imagined movement (EEG) | Planned |
| C: P300 | Attention to flashing options (EEG) | Stretch goal |

## Setup

Requires macOS, [Ollama](https://ollama.com), and conda.

```bash
conda create -n neurovoice python=3.11 -y
conda activate neurovoice
pip install -r requirements.txt
ollama pull llama3.2
```

## Run

```bash
python -m neurovoice.main
```

## Roadmap

- [x] Core loop (listen → propose → select → speak → log)
- [ ] Personalization from logs + keyword expansion mode
- [ ] EEG input (Mode A artifacts, then Mode B motor imagery)
- [ ] Evaluation of the project at this time + future plans or tangents. 

See [Issues](../../issues) for known limitations and planned features.