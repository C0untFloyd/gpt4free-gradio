from g4f import Provider,ChatCompletion
import g4f

# if provider needs auth parameter
provider_auth_settings = {
    'Bard':{
        'cookie':""
    }
}


def send_chat(selected_model, selected_provider, context_history):
    if selected_provider is not None:
        prov = getattr(g4f.Provider, selected_provider)
        prov.working = True
        auth = None
        if prov.needs_auth:
            auth=provider_auth_settings['Bard']
    else:
        auth=None
        prov=None

    print(f'Using Model {selected_model} provided by {selected_provider}')

    try:
        result = g4f.ChatCompletion.create(model=selected_model, stream=False, provider=prov,
                                           messages=context_history,auth=auth)
        context_history.append({'role': 'assistant', 'content': str(result)})
    except Exception as e:
        print(e)
        result = ''
        context_history = []
    return result, context_history



def get_all_models():
    allmodels = []
    for m in g4f.models.ModelUtils.convert:
        allmodels.append(m)
    allmodels.sort()
    return allmodels

def get_providers_for_model(m):
    providers = []
    model = g4f.models.ModelUtils.convert[m]
    if model.best_provider is not None:
        if type(model.best_provider) is tuple:
            for p in model.best_provider:
                providers.append(p.__name__)
        else:
            prov = model.best_provider
            providers.append(prov.__name__)
    # else:
    #     if model.base_provider is not None:
    #         providers.append(model.base_provider)

    providers.sort()
    return providers
        
def get_provider_info(provider):
    if provider is None:
        return ''
    
    prov = getattr(g4f.Provider, provider)
    auth_str = '🔐' if prov.needs_auth else '🔓'
    working = '✅' if prov.working else '❌'
    info = f'## {prov.url} {working} {auth_str}\n{prov.params}'
    return info





