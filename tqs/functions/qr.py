from datetime import datetime
from tqs.functions import key 
import qrcode
import base64
from io import BytesIO
import json


def generate_qr(queue: int):
    data = {
        'queue': queue,
        'issue_dt': str(datetime.now())
    }
    buffered = BytesIO()
    data = json.dumps(data)
    data= key.encrypt(data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    qr_code = 'data:image/png;base64,'+img_str

    # return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPgAAAD4CAIAAABOs7xcAAAABnRSTlMA/gABAP1bbA07AAAExklEQVR4nO3dQW4kKRQA0alR3//KnguYBSNooOK9bVvltBVi8U3//Pz8/PwD3+7f0w8Af4PQSRA6CUInQegkCJ0EoZPwZ/QPn8/nbz7H/zb6O8Do+V//+lmr/k7yeg9OdBKEToLQSRA6CUInQegkCJ2E4Rx95NT99dk57ivPOWvV3H12rj/7PLvN/rxOdBKEToLQSRA6CUInQegkCJ2E6Tn6yCv3p2c//9Q97N3z8t1u68GJToLQSRA6CUInQegkCJ0EoZOwbI5+m1Vz6Ffm7rNqe/Gd6CQInQShkyB0EoROgtBJEDoJXztHH/nWufhIbV4+4kQnQegkCJ0EoZMgdBKEToLQSVg2R79tXntqr8iqfTIju99LusptPTjRSRA6CUInQegkCJ0EoZMgdBKm5+i3zWtnnXpP5+6vn/X6/vhZTnQShE6C0EkQOglCJ0HoJAidhM9t94Z32z2fnv2+s3bfR//WHpzoJAidBKGTIHQShE6C0EkQOgnDOfor96dHTt2rfuW++OvPOfv1TnQShE6C0EkQOglCJ0HoJAidhOFel9vuZ+/ex7LKqnnwqs9f9Tm7f2+7v68TnQShkyB0EoROgtBJEDoJQidh2XtGR1bNa3fPfW/bZ7L7eU7Ny0/9/cSJToLQSRA6CUInQegkCJ0EoZMwvR/91L3kkdvec3nb3ptX9vbs5kQnQegkCJ0EoZMgdBKEToLQSVh2H333/PW2ue+pfe2jz7ntfvmpvUD2o5MmdBKEToLQSRA6CUInQegkDOfou9+7+fqcePbrTz3/K3b/HpzoJAidBKGTIHQShE6C0EkQOgnH3jM667Z95986F3/l/rr96PALoZMgdBKEToLQSRA6CUInYbgf/fX3ep6aZ++er3/r/vjdnOgkCJ0EoZMgdBKEToLQSRA6CdP30VfN10/tO7/tPZqn7rXvnsffti/fiU6C0EkQOglCJ0HoJAidBKGTMLyPvv0bH5qnzn7OyKl7/KueZ9Xn3HY/3hydNKGTIHQShE6C0EkQOglCJ2HZe0Z3z4lfmU+fur++6nNuuwc/Yj86/ELoJAidBKGTIHQShE6C0ElYdh/91D71U/PsWbv3x5+63//K79+JToLQSRA6CUInQegkCJ0EoZMw/Z7RWa/M6W/zre9hHdk9p3eikyB0EoROgtBJEDoJQidB6CQc24++2237vG+7l7/7Hvlte3Wc6CQInQShkyB0EoROgtBJEDoJy/ajn3Jq7vvKHvRVVs3dT/1cTnQShE6C0EkQOglCJ0HoJAidhOm9LqfmoLc9z8htz3nq7wO37b93opMgdBKEToLQSRA6CUInQegkDO+jz7ptn/qs1+fNq+z+fwjuo8NGQidB6CQInQShkyB0EoROwrI5+uteeV/p7P3sVfvgV/1+Vj2//ejwC6GTIHQShE6C0EkQOglCJ+Fr5+i3vR90956TWbe9B3Rk1XM60UkQOglCJ0HoJAidBKGTIHQSls3Rb9tTvnvvyqo5921z6N2fv/s+/YgTnQShkyB0EoROgtBJEDoJQidheo5+256Tkd3v+7ztXvjI7nvtp95Ta68L/ELoJAidBKGTIHQShE6C0En43HaPHHZwopMgdBKEToLQSRA6CUInQegk/Ae/VRgaa0vfQAAAAABJRU5ErkJggg=='

    return qr_code