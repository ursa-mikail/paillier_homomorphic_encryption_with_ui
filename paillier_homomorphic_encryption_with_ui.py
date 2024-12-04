#!pip install libnum
import ipywidgets as widgets
from IPython.display import display, Markdown

import math
from random import randint
import libnum
import sys

# Function to display parameter explanations
def explain_param(parameter):
    explanations = {
        'p': "The first prime number (p). This is used in the key generation process. It must be a large prime number.",
        'q': "The second prime number (q). This is used in conjunction with p to form the public key.",
        'm': "The message to be encrypted. This is the plaintext value that you want to encrypt.",
        'g': "The generator (g). This value must be chosen such that it is relatively prime to n^2.",
        'r': "A random number (r) used in the encryption process to ensure probabilistic encryption."
    }
    if parameter in explanations:
        display(Markdown(f"### {parameter} - Explanation\n{explanations[parameter]}"))

# Set initial parameters with widgets
p_widget = widgets.IntText(value=17, description='Prime p:', tooltip='First prime number (p)', style={'description_width': 'initial'})
q_widget = widgets.IntText(value=19, description='Prime q:', tooltip='Second prime number (q)', style={'description_width': 'initial'})
m_widget = widgets.IntText(value=10, description='Message m:', tooltip='The message to encrypt', style={'description_width': 'initial'})
g_widget = widgets.IntText(value=20, description='Generator g:', tooltip='Generator (g) used in encryption', style={'description_width': 'initial'})
r_widget = widgets.IntText(value=25, description='Random r:', tooltip='Random number used in encryption', style={'description_width': 'initial'})

# Display the widgets
display(p_widget, q_widget, m_widget, g_widget, r_widget)

# Button to show help for each parameter
def on_button_click(param):
    explain_param(param)

p_help_button = widgets.Button(description="Help for p")
q_help_button = widgets.Button(description="Help for q")
m_help_button = widgets.Button(description="Help for m")
g_help_button = widgets.Button(description="Help for g")
r_help_button = widgets.Button(description="Help for r")

# Attach the on_button_click function to each button
p_help_button.on_click(lambda x: on_button_click('p'))
q_help_button.on_click(lambda x: on_button_click('q'))
m_help_button.on_click(lambda x: on_button_click('m'))
g_help_button.on_click(lambda x: on_button_click('g'))
r_help_button.on_click(lambda x: on_button_click('r'))

# Display help buttons
display(p_help_button, q_help_button, m_help_button, g_help_button, r_help_button)


n = p * q
n2 = n * n

# Function to find all values that are coprime with n^2
def find_valid_g_values(n2):
    valid_g = []
    for g in range(1, n2):
        if math.gcd(g, n2) == 1:
            valid_g.append(g)
    return valid_g

# Finding valid g values for Z*_n^2
valid_g_values = find_valid_g_values(n2)

# Output the results
print(f"Value of n: {n}")
print(f"Value of n^2: {n2}")
print(f"The valid g values are: {valid_g_values[:100]}")  # Displaying the first 100 valid g values
print(f"The number of valid g values is: {len(valid_g_values)}")


# Encrypt and decrypt function using the parameters from the widgets
def encrypt_decrypt():
    p = p_widget.value
    q = q_widget.value
    m = m_widget.value
    g = g_widget.value
    r = r_widget.value
    
    # Check if p and q are the same
    if p == q:
        print("P and Q cannot be the same")
        return
    
    # Generate n = p * q, which will be part of the public key
    n = p * q
    
    def L(x,n):
        return ((x-1)//n)
 
    # Compute gLambda using the least common multiple (LCM) of (p-1) and (q-1)
    def gcd(a, b):
        """Compute the greatest common divisor of a and b"""
        while b > 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        """Compute the lowest common multiple of a and b"""
        return a * b // gcd(a, b)
    
    gLambda = lcm(p-1, q-1)
    
    g = randint(20,150)

    if (gcd(g,n*n)==1):
      print("g is relatively prime to n*n")
    else:
      print("WARNING: g is NOT relatively prime to n*n. Will not work!!!")
      print("Try again ...")
      print("=========================================")
      encrypt_decrypt()
 
    r = randint(20,150)
    l = (pow(g, gLambda, n*n)-1)//n
    gMu = libnum.invmod(l, n)

    # Encrypting a message using a random r value
    k1 = pow(g, m, n*n)  # g^m mod n^2
    k2 = pow(r, n, n*n)  # r^n mod n^2
    cipher = (k1 * k2) % (n*n)
    
    # Decrypt the message
    l = (pow(cipher, gLambda, n*n) - 1) // n
    # gMu = (l * pow(r, n, n*n)) % n
    decrypted_message = (l * gMu) % n

    # Output results
    print(f"Public Key (n, g): ({n}, {g})")
    print(f"Private Key (lambda, mu): ({gLambda}, {gMu})")
    print(f"Original message: {m}")
    print(f"Ciphertext: {cipher}")
    print(f"Decrypted message: {decrypted_message}")

# Button to run encryption/decryption
run_button = widgets.Button(description="Encrypt/Decrypt")
run_button.on_click(lambda x: encrypt_decrypt())
display(run_button)

