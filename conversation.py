from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

class ConversationHandler:
    def __init__(self):
        # Initialize GPT-Neo model for conversation
        self.model_name = 'EleutherAI/gpt-neo-125M'  # Using smaller model for local usage
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Conversation context
        self.context = []
        
    def generate_response(self, user_input):
        # Add user input to context
        self.context.append(f"User: {user_input}")
        
        # Prepare prompt with context
        prompt = "\n".join(self.context[-5:]) + "\nAssistant:"
        
        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=150,
            num_return_sequences=1,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("Assistant:")[-1].strip()
        
        # Add response to context
        self.context.append(f"Assistant: {response}")
        
        return response
    
    def clear_context(self):
        self.context = []
