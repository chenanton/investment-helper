"""
Investment Helper (2020)

A web application which suggests personalized stock investments, 
using a machine learning model trained on historical market activity.

Repository link: https://github.com/azychen/investment-helper

Contributors: 

    Anton Chen (https://github.com/azychen)
    Annie Liu (https://github.com/annieliu10)

This file defines the model and any necessary auxiliary functions. 
"""
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, TimeDistributed
from time import time
import os

# Disable tensorflow warnings
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Hyperparameters
model_name = "investment-helper-lstm-{}".format(int(time()))
checkpoint_path = "logs/checkpoints/checkpoint.keras"

training_size = 2000000
batch_size = 512
epochs = 10
num_files = 4


# Beginning and end of sequence sentinel markers
# Currently are placeholder values
XBOS = 1
XEOS = 2
YBOS = 3
YEOS = 4


"""
TRAINING MODEL:

- The training model is a stacked LSTM encoder-decoder network.
- Takes an input of company stock prices before a given time (as a sequence)
- Takes an output of company stock prices after the given time (a sequence as well)
"""

def create_models(T_x, T_y, input_vocab_len, output_vocab_len, embed_dim=128, hidden_dim=512):
    """
    Creates the main structure of the three main models:
        Training model (model_train): 
            - The model trained on the dataset
        Encoder model (model_enc): 
            - Takes prediction input
            - Outputs hidden states (h, c) summarizing inputs
        Decoder model (model_dec): 
            - Takes input of previous timestep output sequence with hidden states h, c 
            - Outputs next timestep sequence
    Note that all models share the same layers, 
    so training model_train also trains layers in both model_enc and model_dec
    """
    # Create  layers
    enc_layers = create_encoder_layers(T_x, input_vocab_len, embed_dim, hidden_dim)
    dec_layers = create_decoder_layers(T_y, output_vocab_len)

    # Connect layers for training model
    enc_output = connect_encoder(enc_layers)
    dec_output = connect_decoder(dec_layers, initial_state=enc_output)

    # Create training model
    enc_input = enc_layers["enc_input"]
    dec_input = dec_layers["dec_input"]
    model_train = Model(inputs=[enc_input, dec_input], outputs=[
                        dec_output], name="model_train")

    model_enc = Model(
        inputs=enc_layers["enc_input"], outputs=enc_output, name="model_enc")

    dec_initial_state = [dec_layers["dec_h"], dec_layers["dec_c"]]
    # re-assign decOutput for decModel
    dec_output = connect_decoder(dec_layers, initial_state=dec_initial_state)
    model_dec = Model(inputs=[dec_input] + dec_initial_state,
                      outputs=dec_output, name="model_dec")

    # Compile model
    model_train.compile(loss="sparse_categorical_crossentropy",
                  optimizer="adam", metrics=["accuracy"])

    return model_train, model_enc, model_dec


def create_encoder_layers(T_x, input_vocab_len, embed_dim=128, hidden_dim=512):
    # Returns dictionary with all layers required in model_enc and first half of model_train.
    layers = {}

    enc_input = Input(shape=(T_x, ), name="enc_input")
    enc_embedding = Embedding(input_dim=input_vocab_len,
                             output_dim=embed_dim, input_length=T_x, name="enc_embedding")
    enc_lstm_0 = LSTM(units=hidden_dim, return_sequences=True, name="enc_lstm_0")
    enc_lstm_1 = LSTM(units=hidden_dim, return_sequences=True, name="enc_lstm_1")
    enc_lstm_2 = LSTM(units=hidden_dim, return_state=True, name="enc_lstm_2")

    layers["enc_input"] = enc_input
    layers["enc_embedding"] = enc_embedding
    layers["enc_lstm_0"] = enc_lstm_0
    layers["enc_lstm_1"] = enc_lstm_1
    layers["enc_lstm_2"] = enc_lstm_2

    return layers


def create_decoder_layers(T_y, output_vocab_len, embed_dim=128, hidden_dim=512):
    # Returns dictionary with all layers required in model_dec and second half of model_train.
    layers = {}

    dec_input = Input(shape=(T_y, ), name="dec_input")
    dec_h = Input(shape=(hidden_dim, ), name="dec_h")
    dec_c = Input(shape=(hidden_dim, ), name="dec_c")

    dec_embedding = Embedding(input_dim=output_vocab_len,
                             output_dim=embed_dim, input_length=T_y, name="dec_embedding")
    dec_lstm_0 = LSTM(units=hidden_dim, return_sequences=True, name="dec_lstm_0")
    dec_lstm_1 = LSTM(units=hidden_dim, return_sequences=True, name="dec_lstm_1")
    dec_lstm_2 = LSTM(units=hidden_dim, return_sequences=True, name="dec_lstm_2")
    dec_dense = TimeDistributed(Dense(output_vocab_len, activation="softmax"), name="dec_dense")

    layers["dec_input"] = dec_input
    layers["dec_h"] = dec_h
    layers["dec_c"] = dec_c
    layers["dec_embedding"] = dec_embedding
    layers["dec_lstm_0"] = dec_lstm_0
    layers["dec_lstm_1"] = dec_lstm_1
    layers["dec_lstm_2"] = dec_lstm_2
    layers["dec_dense"] = dec_dense

    return layers


def connect_encoder(layers):
# Connects encoder layers together
    net = layers["enc_input"]
    net = layers["enc_embedding"](net)
    net = layers["enc_lstm_0"](net)
    net = layers["enc_lstm_1"](net)
    _, h, c = layers["enc_lstm_2"](net)

    enc_output = [h, c]
    return enc_output


def connect_decoder(layers, initial_state):
# Connects decoder layers together
    net = layers["dec_input"]
    net = layers["dec_embedding"](net)
    net = layers["dec_lstm_0"](net, initial_state=initial_state)
    net = layers["dec_lstm_1"](net, initial_state=initial_state)
    net = layers["dec_lstm_2"](net, initial_state=initial_state)
    net = layers["dec_dense"](net)

    dec_output = net
    return dec_output
