from colorama import Fore
from g4f import Provider,ModelUtils,ChatCompletion


# if prover need auth parameter
provider_auth_settings = {
    'Bard':{
        'cookie':""
    }
}

def test_all_providers():
    list_providers = []
    providers = [a for a in dir(Provider) if not a.startswith('__') and a != 'Provider' and a != 'Providers']
    for provider in providers:
        if provider.startswith('Yqcloud'):
            print(Fore.WHITE +f"Skipping Provider {provider}...")
            continue

        print(Fore.WHITE +f"Testing Provider {provider}...")
        # get all model in provider
        models = getattr(Provider,provider).model
        if isinstance(models,str):
            models = [models]
        for model in models:
            print(Fore.WHITE +f"Trying model {model}...")
            provider_llm = getattr(Provider,provider)
            # force provider to testing
            provider_llm.working = True

            model_llm = ModelUtils.convert[model.lower()]
            try:
                # make request
                result = ChatCompletion.create(model=model_llm, stream=False,messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello World!'."
                }
                ],provider=provider_llm,auth=provider_auth_settings['provider'] if provider_llm.needs_auth else None)
                # check if provider and model can response that contain "Hello World"
                if result is not None and result != "" and result != "error" and "Hello World" in result:
                    provideritem = f'{model} provided by {str(provider)}'
                    print(Fore.GREEN+provideritem)
                    list_providers.append(f'{model} provided by {str(provider)}')
                else:
                    print(Fore.RED +f"An exception occurred : {provider} -> {model} -> Result : {result}")
            except Exception as e: 
                print(Fore.RED +f"An exception occurred : {provider} -> {model}")
                print(e)
    print ('Finished testing providers')
    list_providers.sort()
    print(list_providers)
    return list_providers

def get_all_providers():
    list_providers = []
    providers = [a for a in dir(Provider) if not a.startswith('__') and a != 'Provider' and a != 'Providers']
    for provider in providers:
        # get all model in provider
        models = getattr(Provider,provider).model
        if isinstance(models,str):
            models = [models]
        for model in models:
            list_providers.append(f'{model} provided by {str(provider)}')
    list_providers.sort()
    return list_providers

def get_provider_by_name(name: str):
    providers = [a for a in dir(Provider) if not a.startswith('__') and a != 'Provider' and a != 'Providers']
    found =  next(x for x in providers if str(x) == name)
    return found