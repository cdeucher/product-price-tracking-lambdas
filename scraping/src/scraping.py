from kabum import Kabum


def scrap(url):
    if 'kabum' not in url:
        return None, None, None
    kabum = Kabum(url)
    kabum.scrap()
    return kabum.get_price(), kabum.get_title(), kabum.get_image()

if __name__ == '__main__':
    url = "https://www.kabum.com.br/produto/181088/processador-amd-ryzen-5-5600g-3-9ghz-4-4ghz-max-turbo-cache-19mb-6-nucleos-12-threads-video-integrado-am4-100-100000252box"
    price, tittle, image = scrap(url)
    print(f'price: {price}, tittle: {tittle}, image: {image}')
