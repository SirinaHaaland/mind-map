from transformers import GPT2LMHeadModel, GPT2Tokenizer

#initialize tokenizer and model from pretrained GPT2 model from Huggingface
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

#Ask the model anything
sentence = "What is the scariest dinosaur?"
#sentence = "What is AI?"
#sentence = "Generate one topic word for this text: The giraffe is a large African hoofed mammal belonging to the genus Giraffa. It is the tallest living terrestrial animal and the largest ruminant on Earth. Traditionally, giraffes have been thought of as one species, Giraffa camelopardalis, with nine subspecies. Most recently, researchers proposed dividing them into up to eight extant species due to new research into their mitochondrial and nuclear DNA, as well as morphological measurements. Seven other extinct species of Giraffa are known from the fossil record."

#encoding sentence for model to process
inputs = tokenizer.encode(sentence, return_tensors='pt', max_length=800, truncation=True)

#generating text, change max_new_tokens to preferred length of answer from gpt2
outputs = model.generate(inputs, max_new_tokens=200, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

#Calculate the number of tokens in the input sentence
num_input_tokens = len(inputs[0])
#Decode only the generated part, skipping the input tokens
generated_part = outputs[0][num_input_tokens:]
text = tokenizer.decode(generated_part, skip_special_tokens=True)

print("Printing generated answer from gpt2:")
print(text)
