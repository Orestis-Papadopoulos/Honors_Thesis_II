from numpy import array
from pickle import dump
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from data_preparation import*

# load
in_filename = 'republic_sequences.txt'
doc = load_doc(in_filename)
lines = doc.split('\n') # list of sequences

# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines) # integers

# vocabulary size
vocab_size = len(tokenizer.word_index) + 1

# separate into input and output
sequences = array(sequences)
X, y = sequences[:,:-1], sequences[:,-1]

# one-hot encoding
y = to_categorical(y, num_classes = vocab_size)
seq_length = X.shape[1]

def define_compile_fit_save_model():
    """
    Creates the neural network and initiates its training.
    """

    # define model
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length = seq_length))
    model.add(LSTM(100, return_sequences = True))
    model.add(LSTM(100))
    model.add(Dense(100, activation = 'relu'))
    model.add(Dense(vocab_size, activation = 'softmax'))
    print(model.summary())

    # compile model
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    # fit model
    model.fit(X, y, batch_size = 128, epochs = 100) # 100 epochs takes about 5 or 6 hours

    # save the model to file
    model.save('model.h5')
    # save the tokenizer
    dump(tokenizer, open('tokenizer.pkl', 'wb'))

#define_compile_fit_save_model()
