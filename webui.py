import time
import gradio as gr
import g4f
from utility.util_providers import get_all_providers, test_all_providers

restart_server = False
live_cam_active = False


def prompt_ai(select_providers: str, prompt: str, chatbot):
    if len(prompt) < 1:
        return '',chatbot
    s = select_providers.split(' provided by ')
    model = s[0]
    # provider = get_provider_by_name(s[1])
    provider = getattr(g4f.Provider,s[1])
    provider.working = True

    try:
        result = g4f.ChatCompletion.create(model=model, stream=False,messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                    ],provider=provider,auth=None)
    except Exception as e:
        result = f'{e}'
    chatbot.append((prompt, result))
    return '',chatbot

def check_providers():
    return gr.Dropdown.update(choices=test_all_providers())


def run():

    available_themes = ["Default", "gradio/glass", "gradio/monochrome", "gradio/seafoam", "gradio/soft", "gstaff/xkcd", "freddyaboulton/dracula_revamped", "ysharma/steampunk"]
    providerlist = get_all_providers()

    providerlist = ['falcon-40b provided by H2o', 'falcon-7b provided by H2o', 'gpt-3.5-turbo provided by Acytoo', 'gpt-3.5-turbo provided by AiService',
                     'gpt-3.5-turbo provided by Wewordle', 'gpt-4 provided by ChatgptAi', 'llama-13b provided by H2o']

    server_name = None
    if server_name is None or len(server_name) < 1:
        server_name = None
    server_port = None


    run_server = True

    while run_server:

        with gr.Blocks(title=f'gpt4free UI', theme='Default', css="span {color: var(--block-info-text-color)}") as ui:
            with gr.Row(variant='panel'):
                    gr.Markdown(f"### [gpt4free Frontend](https://github.com/C0untFloyd/gpt4free-gradio)")
            with gr.Row(variant='panel'):
                select_providers = gr.Dropdown(providerlist, label="Select Model / Provider")
                bt_check_providers = gr.Button("Check and update list", variant='secondary')
            with gr.Row(variant='panel'):
                chatbot = gr.Chatbot(label="Response")
            with gr.Row(variant='panel'):
                user_prompt = gr.Textbox(label="Prompt", placeholder="Hello")
            with gr.Row(variant='panel'):
                bt_send_prompt = gr.Button("Send", variant='primary')
 
            bt_check_providers.click(fn=check_providers, outputs=[select_providers])
            bt_send_prompt.click(fn=prompt_ai, inputs=[select_providers, user_prompt, chatbot], outputs=[user_prompt, chatbot])

        restart_server = False
        try:
            ui.queue().launch(inbrowser=True, server_name=server_name, server_port=server_port, share=False, prevent_thread_lock=True, show_error=True)
        except:
            restart_server = True
            run_server = False
        try:
            while restart_server == False:
                time.sleep(5.0)
        except (KeyboardInterrupt, OSError):
            print("Keyboard interruption in main thread... closing server.")
            run_server = False
        ui.close()




def restart():
    global restart_server
    restart_server = True

if __name__ == '__main__':
    run()

