from flask import Flask
from Manager import manager_bp
# maybe will be used later
# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone
app = Flask(__name__)
app.register_blueprint(manager_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5095)

app = Flask(__name__)

# @app.route('/comunication_collector_manager', methods=['POST'])
# def comunication_collector_manager():
#     # Obtém os dados do corpo da solicitação
#     # data = json.loads(request.body.decode("utf-8"))
#     """
#     Os dados estão voltando no formato:
#         { 1(projeto_id) : { 1(tag_id) : json_resposta_da_url,
#                             2(tag_id) : json_reposta_da_url2}
#         }
#     """
#
#     # Salva os dados no banco de dados
#     for (key, inner_data) in data.items():
#         # for (inner_key, tag_data) in inner_data.items():
#         #     tag_id = inner_key
#         #     save_value = ""
#         #     try:
#         #         if tag_id == '1':
#         #             save_value = tag_data["value"]
#         #         elif tag_id == '2':
#         #             save_value = tag_data["data"][0]
#         #         elif tag_id == '3':
#         #             save_value = tag_data["results"][0]["question"]
#         #     except:
#         #         print(f"Erro ao salvar tag: {tag_id}")
#         #     actual_project = self.get_project_by_id(key)
#         #     actual_tag = self.get_tag_by_id(tag_id)
#         #     if save_value:
#         #         temp = ProjectTag(projeto=actual_project, tag=actual_tag, value=save_value) #Escreve no banco de dados
#         #         temp.save() #Salva no banco de dados
#         #     print(f"Project ID: {key}, tag id: {tag_id} value: {save_value}")
#
#         # purge_old_data()
#         return jsonify({}, status=200)
#
# @app.route('/comunication_collector_manager', methods=['GET'])
# def comunication_collector_manager():
#     # Consulta no banco de dados os dados que precisam de update
#     update_list = {}
#     # projects = self.get_all_projects()
#     # tags = self.get_all_tags()
#     # for project in projects:
#     #     project_update = {}
#     #     for tag in tags:
#     #         latest_row = self.get_recent_value_for_project_and_tag(project.id, tag.tag_id)
#     #         latest_time = latest_row.timestamp if latest_row else None
#
#     #         if latest_time is None or latest_time < (datetime.now(timezone.utc) - timedelta(seconds=30)):
#     #             project_update[tag.tag_id] = {
#     #                 "tag_lastime": latest_time
#     #             }
#
#     #     update_list[project.id] = {
#     #         "tags": project_update,
#     #         "link": project.link
#     #     }
#
#
#     return jsonify(update_list, status=200)