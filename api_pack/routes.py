from api_pack import app


@app.route("/<numero>", methods=['GET','POST'])
def home(numero):
    dic = {}
    dic['resultado'] = 100 * int(numero)
    return dic