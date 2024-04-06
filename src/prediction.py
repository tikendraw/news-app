from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class PredictionPipeline:
    def __init__(self, model_path="bart-samsum-model", tokenizer_path="tokenizer"):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.pipe = pipeline(
            "summarization", model=self.model, tokenizer=self.tokenizer
        )
        self.max_input_length = self.model.config.max_position_embeddings

    def split_text(self, text):
        sentences = text.split(". ")
        chunks = []
        current_chunk = []
        total_length = 0

        for sentence in sentences:
            sentence_length = len(self.tokenizer.encode(f" {sentence}"))
            if total_length + sentence_length > self.max_input_length:
                chunks.append(". ".join(current_chunk) + ".")
                current_chunk = [sentence]
                total_length = sentence_length
            else:
                current_chunk.append(sentence)
                total_length += sentence_length

        if current_chunk:
            chunks.append(". ".join(current_chunk) + ".")

        return chunks

    def predict(self, text):
        gen_kwargs = {"length_penalty": 0.8, "num_beams": 8, "max_length": 300}
        chunks = self.split_text(text)
        summaries = []

        for chunk in chunks:
            output = self.pipe(chunk, **gen_kwargs)[0]["summary_text"]
            summaries.append(output)

        summary = " ".join(summaries)
        print("\nModel Summary:")
        print(summary)

        return summary
