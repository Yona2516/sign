import tensorflow as tf

model = tf.saved_model.load("C:/Users/SphB\PycharmProjects/signlanguagedetectionhospital/model/lstm_model.pt")
print("Available signatures:", list(model.signatures.keys()))

signature = model.signatures.get('serving_default')
if signature:
    print("Inputs:")
    print(signature.structured_input_signature)
    print("Outputs:")
    print(signature.structured_outputs)
else:
    print("No 'serving_default' signature found.")
