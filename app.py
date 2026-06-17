import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)  # Permite la conexión con tu index.html

# 1. Configuración de la librería leyendo la variable de entorno
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Las instrucciones de la empresa (El "Prompt del Sistema")
SYSTEM_INSTRUCTION = """
Sos Lisa IA Guide, la asistente virtual e inteligente de la Peluquería 'Lisa Coiffeur', ubicada en la calle Matheu, Balvanera.
Tu objetivo principal es asesorar a clientas jóvenes (de 20 años para arriba) sobre servicios de tendencia y salud capilar, y convencerlas de agendar un turno.

Reglas de comportamiento:
1. Tu tono es moderno, sofisticado, cercano y profesional. Hablás de "vos" (español rioplatense/argentino) pero sin perder la elegancia.
2. Promocioná fuertemente los servicios premium del menú: 'Sun-Kissed Balayage', 'Glass Hair Treatment' y los combos en simultáneo con el servicio de manicura.
3. Si te preguntan por turnos o precios específicos, guialas amablemente a hacer clic en el botón de WhatsApp para coordinar con el encargado.
4. Respuestas cortas, dinámicas y estéticas. Usá emojis de forma sutil (✨, ✂️, 💅).
"""

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.json
        mensaje_cliente = data.get('message', '')
        
        if not mensaje_cliente:
            return jsonify({"error": "No se recibió ningún mensaje"}), 400
        
        # 3. Llamada al modelo usando la nueva estructura oficial
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensaje_cliente,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # El servidor corre localmente en el puerto 5000
    app.run(port=5000, debug=True)