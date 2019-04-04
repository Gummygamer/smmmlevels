import numpy as np
import six
import tensorflow as tf
import time
import os
import sys 
from tensorflow import keras
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

SHAKESPEARE_TXT = 'strlvl'


def transform(txt, pad_to=None):
  # drop any non-ascii characters
  output = np.asarray([ord(c) for c in txt if ord(c) < 255], dtype=np.int32)
  if pad_to is not None:
    output = output[:pad_to]
    output = np.concatenate([
        np.zeros([pad_to - len(txt)], dtype=np.int32),
        output,
    ])
  return output

def training_generator(seq_len=100, batch_size=1024):
  """A generator yields (source, target) arrays for training."""
  with open(SHAKESPEARE_TXT, 'r') as f:
    txt = f.read()

  source = transform(txt)
  while True:
    offsets = np.random.randint(0, len(source) - seq_len, batch_size)

    # Our model uses sparse crossentropy loss, but Keras requires labels
    # to have the same rank as the input logits.  We add an empty final
    # dimension to account for this.
    yield (
        np.stack([source[idx:idx + seq_len] for idx in offsets]),
        np.expand_dims(
            np.stack([source[idx + 1:idx + seq_len + 1] for idx in offsets]),
            -1),
    )

six.next(training_generator(seq_len=1, batch_size=10))

EMBEDDING_DIM = 512
seq_len=1
batch_size=10
steps_per_epoch=150
epochs=10

def lstm_model(seq_len, batch_size=None, stateful=True):
  """Language model: predict the next word given the current word."""
  source = tf.keras.Input(
      name='seed', shape=(seq_len,), batch_size=batch_size, dtype=tf.int32)

  embedding = tf.keras.layers.Embedding(input_dim=256, output_dim=EMBEDDING_DIM)(source)
  lstm_1 = tf.keras.layers.LSTM(EMBEDDING_DIM, stateful=stateful, return_sequences=True)(embedding)
  lstm_2 = tf.keras.layers.LSTM(EMBEDDING_DIM, stateful=stateful, return_sequences=True)(lstm_1)
  predicted_char = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(256, activation='softmax'))(lstm_2)
  model = tf.keras.Model(inputs=[source], outputs=[predicted_char])
  model.compile(
      optimizer=tf.optimizers.RMSprop(learning_rate=0.01),
      loss='sparse_categorical_crossentropy',
      metrics=['sparse_categorical_accuracy'])
  return model

tf.keras.backend.clear_session()

training_model = lstm_model(seq_len, batch_size, stateful=False)

training_model.fit_generator(
    training_generator(seq_len, batch_size),
    steps_per_epoch,
    epochs,
)

try:
    os.mkdir(os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs))
except OSError:  
    print ("Creation of the directory %s failed" % os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs))
else:  
    print ("Successfully created the directory %s " % os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs))

training_model.save(os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs)+'/model.h5', overwrite=True)


BATCH_SIZE = 10
PREDICT_LEN = 6480

# Keras requires the batch size be specified ahead of time for stateful models.
# We use a sequence length of 1, as we will be feeding in one character at a 
# time and predicting the next character.
prediction_model = keras.models.load_model(os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs)+'/model.h5')
#prediction_model = lstm_model(seq_len=1, batch_size=BATCH_SIZE, stateful=True)
#prediction_model.load(os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs)+'/model.h5')



# We seed the model with our initial string, copied BATCH_SIZE times

seed_txt = "'"
seed = transform(seed_txt)
seed = np.repeat(np.expand_dims(seed, 0), BATCH_SIZE, axis=0)

# First, run the seed forward to prime the state of the model.
prediction_model.reset_states()
for i in range(len(seed_txt) - 1):
  prediction_model.predict(seed[:, i:i + 1])

# Now we can accumulate predictions!
predictions = [seed[:, -1:]]
for i in range(PREDICT_LEN):
  last_word = predictions[-1]
  next_probits = prediction_model.predict(last_word)[:, 0, :]
  
    # sample from our output distribution
  next_idx = [
     np.random.choice(256, p=next_probits[i])
     for i in range(BATCH_SIZE)
  ]
  predictions.append(np.asarray(next_idx, dtype=np.int32))
  

for i in range(BATCH_SIZE):
  p = [predictions[j][i] for j in range(PREDICT_LEN)]
  generated = ''.join([chr(c) for c in p])
  text_file = open(os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs)+"/levelN"+str(i)+".txt", "w")
  text_file.write("%s" % generated)
  text_file.close()
  print(len(generated))
  assert len(generated) == PREDICT_LEN, 'Generated text too short'
