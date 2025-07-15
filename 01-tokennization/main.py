import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, I am Rameshwar Mane"
tokens = enc.encode(text)
print("Tokens:", tokens)

Tokens= [13225, 11, 357, 939, 460, 1463, 71, 9126, 119328]

decoded_text = enc.decode(tokens)
print("Decoded Text:", decoded_text)