# """
# =============================================================
#   Plant Disease Detection - Flask Web Application
# =============================================================
#   Run this file to start the web server:
#     python app.py

#   Then open: http://localhost:5000
# """

# import os
# import sys
# import uuid
# import base64
# from pathlib import Path
# from flask import Flask, request, jsonify, render_template, send_from_directory
# from werkzeug.utils import secure_filename

# # Add project root to path
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# from utils.predictor import predict, load_model_and_labels, DISEASE_INFO

# # ─── Flask App Setup ──────────────────────────────────────────────────────────
# app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16MB max upload
# app.config['UPLOAD_FOLDER'] = 'static/uploads'

# # Allowed image types
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # ─── Routes ───────────────────────────────────────────────────────────────────

# @app.route('/')
# def index():
#     """Serve the main page."""
#     return render_template('index.html')


# @app.route('/api/predict', methods=['POST'])
# def predict_disease():
#     """
#     API endpoint for disease prediction.

#     Accepts:
#       - multipart/form-data with 'image' field (file upload)
#       - JSON with 'image_base64' field (base64 encoded image)

#     Returns JSON:
#       {
#         "success": true,
#         "result": { ... prediction data ... }
#       }
#     """
#     try:
#         image_bytes = None

#         # ── Handle file upload ────────────────────────────────────────────────
#         if 'image' in request.files:
#             file = request.files['image']
#             if file.filename == '':
#                 return jsonify({"success": False, "error": "No file selected"}), 400
#             if not allowed_file(file.filename):
#                 return jsonify({"success": False,
#                                 "error": "Invalid file type. Use PNG, JPG, JPEG, GIF, BMP, or WEBP"}), 400
#             image_bytes = file.read()

#         # ── Handle base64 upload ──────────────────────────────────────────────
#         elif request.is_json and 'image_base64' in request.json:
#             b64 = request.json['image_base64']
#             if ',' in b64:           # Strip data URL prefix if present
#                 b64 = b64.split(',')[1]
#             image_bytes = base64.b64decode(b64)

#         else:
#             return jsonify({"success": False,
#                             "error": "No image provided. Send 'image' file or 'image_base64' JSON field"}), 400

#         # ── Run prediction ────────────────────────────────────────────────────
#         result = predict(image_bytes)

#         return jsonify({
#             "success": True,
#             "result": result
#         })

#     except Exception as e:
#         app.logger.error(f"Prediction error: {str(e)}", exc_info=True)
#         return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500


# @app.route('/api/diseases', methods=['GET'])
# def list_diseases():
#     """API endpoint — list all supported diseases."""
#     diseases = []
#     for class_name, info in DISEASE_INFO.items():
#         if class_name != "default":
#             diseases.append({
#                 "class_name": class_name,
#                 "display_name": info["display_name"],
#                 "type": info["type"],
#                 "severity": info["severity"],
#                 "plant": class_name.split("___")[0].replace("_", " ") if "___" in class_name else "Various",
#                 "emoji": info.get("emoji", "🌿")
#             })
#     return jsonify({"success": True, "count": len(diseases), "diseases": diseases})


# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """API health check endpoint."""
#     model, labels = load_model_and_labels()
#     return jsonify({
#         "status": "ok",
#         "model_loaded": model is not None,
#         "labels_loaded": labels is not None,
#         "num_classes": len(labels) if labels else 0
#     })


# @app.route('/static/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# # ─── Startup ──────────────────────────────────────────────────────────────────
# if __name__ == '__main__':
#     # Create uploads directory if it doesn't exist
#     Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
#     Path('model').mkdir(exist_ok=True)

#     print("=" * 60)
#     print("  🌿 Plant Disease Detection App")
#     print("=" * 60)
#     print(f"  🌐 Open in browser: http://localhost:5000")
#     print(f"  📡 API endpoint:    http://localhost:5000/api/predict")
#     print(f"  🔍 Disease list:    http://localhost:5000/api/diseases")
#     print("=" * 60)

#     # Pre-load model at startup
#     load_model_and_labels()

#     app.run(debug=True, host='0.0.0.0', port=5000)



"""
=============================================================
  Plant Disease Detection - Flask Web Application
=============================================================
  Run this file to start the web server:
    python app.py

  Then open: http://localhost:5000
"""

import os
import sys
import uuid
import base64
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.predictor import predict, load_model_and_labels, DISEASE_INFO

# ─── Flask App Setup ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16MB max upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Allowed image types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """
    API endpoint for disease prediction.

    Accepts:
      - multipart/form-data with 'image' field (file upload)
      - JSON with 'image_base64' field (base64 encoded image)

    Returns JSON:
      {
        "success": true,
        "result": { ... prediction data ... }
      }
    """
    try:
        image_bytes = None

        # ── Handle file upload ────────────────────────────────────────────────
        if 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                return jsonify({"success": False, "error": "No file selected"}), 400
            if not allowed_file(file.filename):
                return jsonify({"success": False,
                                "error": "Invalid file type. Use PNG, JPG, JPEG, GIF, BMP, or WEBP"}), 400
            image_bytes = file.read()

        # ── Handle base64 upload ──────────────────────────────────────────────
        elif request.is_json and 'image_base64' in request.json:
            b64 = request.json['image_base64']
            if ',' in b64:           # Strip data URL prefix if present
                b64 = b64.split(',')[1]
            image_bytes = base64.b64decode(b64)

        else:
            return jsonify({"success": False,
                            "error": "No image provided. Send 'image' file or 'image_base64' JSON field"}), 400

        # ── Run prediction ────────────────────────────────────────────────────
        result = predict(image_bytes)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500


@app.route('/api/disease-detail', methods=['GET'])
def disease_detail():
    """
    Return full disease info for a given class name.
    Usage: GET /api/disease-detail?class=Tomato___Early_blight
    """
    class_name = request.args.get('class', '')
    if not class_name:
        return jsonify({"success": False, "error": "No class name provided"}), 400

    from utils.predictor import get_disease_info, DISEASE_INFO
    info = get_disease_info(class_name)

    # Derive plant name from class_name
    plant = class_name.split('___')[0].replace('_', ' ') if '___' in class_name else 'Various'

    return jsonify({
        "success": True,
        "class_name": class_name,
        "plant": plant,
        **info
    })


@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    """API endpoint — list all supported diseases."""
    diseases = []
    for class_name, info in DISEASE_INFO.items():
        if class_name != "default":
            diseases.append({
                "class_name": class_name,
                "display_name": info["display_name"],
                "type": info["type"],
                "severity": info["severity"],
                "plant": class_name.split("___")[0].replace("_", " ") if "___" in class_name else "Various",
                "emoji": info.get("emoji", "🌿")
            })
    return jsonify({"success": True, "count": len(diseases), "diseases": diseases})


@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check endpoint."""
    model, labels = load_model_and_labels()
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "labels_loaded": labels is not None,
        "num_classes": len(labels) if labels else 0
    })


@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ─── Startup ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path('model').mkdir(exist_ok=True)

    print("=" * 60)
    print("  🌿 Plant Disease Detection App")
    print("=" * 60)
    print(f"  🌐 Open in browser: http://localhost:5000")
    print(f"  📡 API endpoint:    http://localhost:5000/api/predict")
    print(f"  🔍 Disease list:    http://localhost:5000/api/diseases")
    print("=" * 60)

    # Pre-load model at startup
    load_model_and_labels()

    app.run(debug=True, host='0.0.0.0', port=5000)