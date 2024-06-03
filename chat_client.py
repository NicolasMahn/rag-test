import gradio as gr
import yaml

import query_data


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)


def main():
    config = load_config("config.yaml")
    data_topics = config['data_topics']
    default_topic = config['default_topic']

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--reset", action="store_true", help="Reset the database.")
    #parser.add_argument("--debug", action="store_true", help="Additional print statements")
    #parser.add_argument("--topic", choices=data_topics.keys(), help="Select the data topic.")
    #args = parser.parse_args()

    #selected_topic = args.topic if args.topic else default_topic
    topic_config = data_topics[default_topic]
    topic_dir = topic_config['topic_dir']

    Chat_client(topic_dir).launch_chat_client()


class Chat_client:
    def __init__(self, topic_dir: str):
        self.topic_dir = topic_dir
        self.chroma_dir = f"{self.topic_dir}/chroma"
        self.data_dir = f"{self.topic_dir}/documents"

    def chat_function(self, message: str, history: list):
        response = query_data.query_rag(message, self.data_dir, self.chroma_dir)

        return response

    def launch_chat_client(self):
        gr.ChatInterface(
            fn=self.chat_function,
            chatbot=gr.Chatbot(height=900, placeholder="Ask me any question about the Panda robot!"),
            title="Production knowledgebase",
            description="Ask me any question about the Panda robot!",
            theme="soft",
            examples=["Test1", "Test2", "Test3"],
            cache_examples=True,
            retry_btn=None,
            undo_btn="Delete Previous",
            clear_btn="Clear"
        ).launch()

if __name__ == "__main__":
    main()
