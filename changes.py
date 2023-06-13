import requests
import geojson
import html
def changefunc(changes,tags):
    changes_list=[]
    openstreeturl="https://www.openstreetmap.org/{}/{}"
    if tags:
        k, v = tags.split('=')
    changeset_base_url="https://s3.amazonaws.com/mapbox/real-changesets/production"
    for feature in changes:
        changeset_id = str(feature['id'])
        changeset_url = f"{changeset_base_url}/{changeset_id}.json"
        date = feature['properties']['date']

        response = requests.get(changeset_url)
        changeset_data = response.json()

        for x in changeset_data['elements']:
            new_geometry = []
            old_geometry = []
            if x['changeset'] == changeset_id:
                feature_id = x['id']
                if 'tags' in x:            
                    n_tags = x['tags']
                    if isinstance(n_tags, str):
                        try:
                            n_tags = ast.literal_eval(n_tags.replace("'", '"'))
                        except (ValueError, SyntaxError):
                            n_tags = {}
                else:
                    n_tags = {}

                if 'old' in x:
                    old_tags = x['old']['tags']
                    if isinstance(old_tags, str):
                        try:
                            old_tags = ast.literal_eval(old_tags.replace("'", '"'))
                        except (ValueError, SyntaxError):
                            old_tags = {}
                else:
                    old_tags = {}

                if 'name:en' in x['tags']:
                    name_value = x['tags']['name:en']
                else:
                    name_value = "-"


                coordinates = []
                old_coordinates = []
                if 'nodes' in x:
                    for node in x["nodes"]:
                        coordinates.append((float(node["lon"]), float(node["lat"])))

                if 'old' in x and 'nodes' in x['old']:
                    for node in x['old']["nodes"]:
                        old_coordinates.append((float(node["lon"]), float(node["lat"])))

                geometry = geojson.LineString(coordinates) if x["type"] == "way" else geojson.Polygon([coordinates])
                feature_geojson = geojson.Feature(geometry=geometry, properties={})
                new_geometry.append(feature_geojson)

                geometry_1 = geojson.LineString(old_coordinates) if x["type"] == "way" else geojson.Polygon([old_coordinates])
                feature_geojson = geojson.Feature(geometry=geometry_1, properties={})
                old_geometry.append(feature_geojson)
                geometry_changed = "No"
                if coordinates != old_coordinates:
                    geometry_changed = "Yes"
                

                if any(key == k and value == v for key, value in old_tags.items()):
                    changes = {
                        'changeset_id': x['changeset'],
                        'feature_id': feature_id,
                        'user': x['user'],
                        'user_id': x['uid'],
                        'action': x['action'],
                        'type': x.get('type', ''),
                        'old_tags': old_tags,
                        'new_tags': n_tags,
                        'date': date,
                        'name': name_value,
                        'geometry_changed': geometry_changed,
                        'viewOSM': openstreeturl.format(html.escape(x['type']), feature_id)
                    }
                    if geometry_changed == "Yes":
                        changes['new_geometry'] = new_geometry
                        changes['old_geometry'] = old_geometry
                    else:
                        changes['new_geometry'] = new_geometry
                    changes_list.append(changes)
    
                elif any(key == k and value == v for key, value in n_tags.items()):
                    changes = {
                        'changeset_id': x['changeset'],
                        'feature_id': feature_id,
                        'user': x['user'],
                        'user_id': x['uid'],
                        'action': x['action'],
                        'type': x.get('type', ''),
                        'old_tags': old_tags,
                        'new_tags': n_tags,
                        'date': date,
                        'name': name_value,
                        'geometry_changed': geometry_changed,
                        'viewOSM': openstreeturl.format(html.escape(x['type']), feature_id)
                    }
                    if geometry_changed == "Yes":
                        changes['new_geometry'] = new_geometry
                        changes['old_geometry'] = old_geometry
                    else:
                        changes['new_geometry'] = new_geometry
                    changes_list.append(changes)

    return(changes_list)