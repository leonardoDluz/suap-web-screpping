from fastapi import FastAPI
from .suap.suap_boletim import SuapBoletim
from .dtos.suap_login_dto import SuapLoginDTO

app = FastAPI()

@app.get('/{username}/boletim')
def boletim(username: str, password: str, period: str):
    try:
        suap_login_info = SuapLoginDTO(username=username, password=password)
        suap_boletim = SuapBoletim(suap_login_info)
        return suap_boletim.get_content(period)
    except Exception as e:
        return e