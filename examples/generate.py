from awq import AutoAWQForCausalLM
from awq.utils.utils import get_best_device
from transformers import AutoTokenizer, TextStreamer


quant_path = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"

# Load model
if get_best_device() == "cpu":
    model = AutoAWQForCausalLM.from_quantized(quant_path, use_qbits=True, fuse_layers=False)
else:
    model = AutoAWQForCausalLM.from_quantized(quant_path, fuse_layers=True)
tokenizer = AutoTokenizer.from_pretrained(quant_path, trust_remote_code=True)
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# Convert prompt to tokens
prompt_template = "[INST] {prompt} [/INST]"

prompt = "You're standing on the surface of the Earth. "\
        "You walk one mile south, one mile west and one mile north. "\
        "You end up exactly where you started. Where are you?"

tokens = tokenizer(
    prompt_template.format(prompt=prompt), 
    return_tensors='pt'
).input_ids
tokens = tokens.to(get_best_device())

# Generate output
generation_output = model.generate(
    tokens, 
    streamer=streamer,
    max_new_tokens=512
)