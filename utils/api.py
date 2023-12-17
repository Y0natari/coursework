import aiohttp

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def create_category(self, name):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/'
            data = {'name': name}
            async with session.post(url, json=data) as response:
                return await response.json()

    async def update_category(self, category_id, new_name):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/{category_id}/'
            data = {'name': new_name}
            async with session.put(url, json=data) as response:
                return await response.json()

    async def delete_category(self, category_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/{category_id}/'
            async with session.delete(url) as response:
                return response.status

    async def get_category_by_id(self, category_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/?id={category_id}'
            async with session.get(url) as response:
                return await response.json()

    async def get_category_name_by_id(self, category_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/{category_id}/'
            async with session.get(url) as response:
                category = await response.json()
                return category['name']

    async def create_drug(self, name, category_id, price, quantity):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/drugs/'
            data = {'name': name, 'category': category_id, 'price': price, 'quantity': quantity}
            async with session.post(url, json=data) as response:
                return await response.json()

    async def get_category_names(self):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/categories/'
            async with session.get(url) as response:
                categories = await response.json()
                return [category['name'] for category in categories]

    async def update_drug(self, drug_id, name=None, category_id=None, price=None, quantity=None):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/drugs/{drug_id}/'
            data = {}
            if name is not None:
                data['name'] = name
            if category_id is not None:
                data['category'] = category_id
            if price is not None:
                data['price'] = price
            if quantity is not None:
                data['quantity'] = quantity
            async with session.put(url, json=data) as response:
                return await response.json()

    async def delete_drug(self, drug_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/drugs/{drug_id}/'
            async with session.delete(url) as response:
                return response.status

    async def get_drug_by_id(self, drug_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/drugs/?id={drug_id}'
            async with session.get(url) as response:
                return await response.json()

    async def get_drugs_by_category(self, category_id):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/drugs/?category_id={category_id}'
            async with session.get(url) as response:
                return await response.json()