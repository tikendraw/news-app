from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline


class PredictionPipeline:
    def __init__(self, model_path="bart-samsum-model", tokenizer_path="tokenizer"):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_path
        )  # Load trained model
        self.pipe = pipeline(
            "summarization", model=self.model, tokenizer=self.tokenizer
        )
        # self.config = ConfigurationManager().get_model_evaluation_config()
        # tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        # pipe = pipeline("summarization", model=self.config.model_path,tokenizer=tokenizer)

    def predict(self, text):
        gen_kwargs = {"length_penalty": 0.8, "num_beams": 8, "max_length": 200}

        print("Dialogue:")
        print(text)

        output = self.pipe(text, **gen_kwargs)[0]["summary_text"]
        print("\nModel Summary:")
        print(output)

        return output


# Example usage (replace with your actual file paths)
if __name__ == "__main__":
    model_path = "bart-samsum-model"  # Update with your model path
    tokenizer_path = "tokenizer"  # Update with your tokenizer path
    model = PredictionPipeline(model_path, tokenizer_path)
    sample_text = """The economy of India has transitioned from a mixed planned economy to a mixed middle-income developing social market economy with notable public sector in strategic sectors.[47] It is the world's fifth-largest economy by nominal GDP and the third-largest by purchasing power parity (PPP); on a per capita income basis, India ranked 139th by GDP (nominal) and 127th by GDP (PPP).[48] From independence in 1947 until 1991, successive governments followed Soviet model and promoted protectionist economic policies, with extensive Sovietization, state intervention, demand-side economics, natural resources, bureaucrat driven enterprises and economic regulation. This is characterised as dirigism, in the form of the Licence Raj.[49][50] The end of the Cold War and an acute balance of payments crisis in 1991 led to the adoption of a broad economic liberalisation in India and indicative planning.[51][52] Since the start of the 21st century, annual average GDP growth has been 6% to 7%.[47] The economy of the Indian subcontinent was the largest in the world for most of recorded history up until the onset of colonialism in early 19th century.[53][54][55]

Nearly 70% of India's GDP is driven by domestic consumption;[56] country remains the world's sixth-largest consumer market.[57] Apart from private consumption, India's GDP is also fueled by government spending, investments, and exports.[58] In 2022, India was the world's 8th-largest importer and the 10th-largest exporter.[59] India has been a member of the World Trade Organization since 1 January 1995.[60] It ranks 63rd on the Ease of doing business index and 40th on the Global Competitiveness Index.[61] With 476 million workers, the Indian labour force is the world's second-largest.[20] India has one of the world's highest number of billionaires and extreme income inequality.[62][63]

During the 2008 global financial crisis, the economy faced a mild slowdown. India endorsed Keynesian policy and initiated stimulus measures (both fiscal and monetary) to boost growth and generate demand. In subsequent years, economic growth revived.[64] The period between 2004 and 2014 is referred to as India's lost decade as India fell behind other BRIC economies.[65][66]

In 2021–22, the foreign direct investment (FDI) in India was $82 billion. The leading sectors for FDI inflows were the service sector, the computer industry, and the telecom industry.[67] India has free trade agreements with several nations and blocs, including ASEAN, SAFTA, Mercosur, South Korea, Japan, Australia, UAE, and several others which are in effect or under negotiating stage.[68][69]

The service sector makes up more than 50% of GDP and remains the fastest growing sector, while the industrial sector and the agricultural sector employs a majority of the labor force.[70] The Bombay Stock Exchange and National Stock Exchange are some of the world's largest stock exchanges by market capitalisation.[71] India is the world's sixth-largest manufacturer, representing 2.6% of global manufacturing output.[72] Nearly 65% of India's population is rural,[73] and contributes about 50% of India's GDP.[74] India faces high unemployment, rising income inequality, and a drop in aggregate demand.[75][76] India's gross domestic savings rate stood at 29.3% of GDP in 2022.[77] In recent years, independent economists and financial institutions have accused the government of manipulating various economic data, especially GDP growth.[78][79] India's overall social spending as a share of GDP in 2021–22 will be 8.6%, which is much lower than the average for OECD nations.[80][81]"""
    summary = model.predict(sample_text)
    print(f"\nGenerated Summary: {summary}")
