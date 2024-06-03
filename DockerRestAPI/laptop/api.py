# Laptop Service

from flask import Flask, request, abort, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient, ASCENDING

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# connect to mongoDB database
#this connects to a MongoDB server on the local machine
client = MongoClient('db', 27017)
#creates a database object that represents tododb database 
db = client.tododb

class Laptop(Resource):
    def get(self):
        return {
            'Laptops': ['Mac OS', 'Dell', 
            'Windozzee',
      'Yet another laptop!',
      'Yet yet another laptop!'
            ]
        }


#json request
class handle_functionalities(Resource):
    def get_query(self):
        top = request.args.get('top')
        print("top is" + str(top))

        if top is None:
            default = 20
            return default
        else:
            return int(top) + 1
   

    def get_brevet_info(self):

        brevet_doc = db.tododb.find_one({'brevet_distance': {'$exists': True}})
        
        if brevet_doc:
            begin_time = brevet_doc['begin_time']
            begin_date = brevet_doc['begin_date']
            brevet_distance = brevet_doc['brevet_distance']
        else:
            begin_time = None
            begin_date = None
            brevet_distance = None

        return {
                'begin_time': begin_time,
                'begin_date': begin_date,
                'brevet_distance': brevet_distance
            }

    def get_format(self, format):
        if format is None:
            return 'json'
        elif format in ['csv', 'json']:
            return format
        else:
            abort(400, description="Invalid format given")


    #get everything to the specified limit
    def get_documents(self, sort_field, limit):
        # list to put documents in
        cursor = db.tododb.find() 
        cursor = cursor.sort(sort_field, ASCENDING)
        cursor = cursor.limit(limit)
        documents = list(cursor)
        print(documents)
        return documents


    #only get what is wanted
    def filter_documents(self, documents, fields):
        filtered_docs = []
        for doc in documents:
            if all(field in doc for field in fields):
                filtered_docs.append(doc)
        return filtered_docs

    #return as json
    def format_json(self, documents, fields, begin_time, begin_date, brevet_distance):
        json_format = {
        'begin_time': begin_time,
        'begin_date': begin_date,
        'brevet_distance': brevet_distance,
        'data': {}
        }
        for field in fields:
            json_format['data'][field] = [doc.get(field) for doc in documents]

        print(json_format)

        return json_format

    #return as csv
    def format_csv(self, documents, fields, begin_time, begin_date, brevet_distance):
        csv_format = ''

        csv_format += f"brevets/distance, brevets/begin_date, brevets/begin_time, "
        for i in range(len(documents)):
            for field in fields:
                csv_format += f"brevets/{i}/{field}, "
        csv_format += '\n '

        csv_format += f"{brevet_distance}, {begin_date}, {begin_time}, "
        for doc in documents:
            csv_format += ', '.join([str(doc.get(field, '')) for field in fields]) + ', '

        return csv_format
    
    
class list_all(handle_functionalities):
    def get(self, format=None):
        limit = self.get_query()
        format = self.get_format(format)

        brevet_info = self.get_brevet_info()
        begin_time = brevet_info['begin_time']
        begin_date = brevet_info['begin_date']
        brevet_distance = brevet_info['brevet_distance']

        documents = self.get_documents("open", limit)
        fields = ['open', 'close']  # Specify the fields you need
        filtered = self.filter_documents(documents, fields)

        if format == 'csv':
            return self.format_csv(filtered, fields, begin_time, begin_date, brevet_distance)
        else:
            return self.format_json(filtered, fields, begin_time, begin_date, brevet_distance)


#handles open only
class list_open_only(handle_functionalities):
    def get(self, format = None):
        limit = self.get_query()
        format = self.get_format(format)

        brevet_info = self.get_brevet_info()
        begin_time = brevet_info['begin_time']
        begin_date = brevet_info['begin_date']
        brevet_distance = brevet_info['brevet_distance']

        documents = self.get_documents("open", limit)
        fields = ['open']
        filtered = self.filter_documents(documents, fields)

        if format == 'csv':
            return self.format_csv(filtered, fields, begin_time, begin_date, brevet_distance)
        else:
            return self.format_json(filtered, fields, begin_time, begin_date, brevet_distance)

#handles close only
class list_close_only(handle_functionalities):
    def get(self, format = None):
        limit = self.get_query()
        format = self.get_format(format)

        brevet_info = self.get_brevet_info()
        begin_time = brevet_info['begin_time']
        begin_date = brevet_info['begin_date']
        brevet_distance = brevet_info['brevet_distance']

        documents = self.get_documents("open", limit)
        fields = ['close']
        filtered = self.filter_documents(documents, fields)

        if format == 'csv':
            return self.format_csv(filtered, fields, begin_time, begin_date, brevet_distance)
        else:
            return self.format_json(filtered, fields, begin_time, begin_date, brevet_distance)

    


api.add_resource(list_all, '/listAll', '/listAll/<string:format>')
api.add_resource(list_open_only, '/listOpenOnly', '/listOpenOnly/<string:format>')
api.add_resource(list_close_only, '/listCloseOnly', '/listCloseOnly/<string:format>')



# Create routes
# Another way, without decorators
api.add_resource(Laptop, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)