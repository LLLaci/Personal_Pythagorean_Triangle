import streamlit as st
import math
from st_keyup import st_keyup

ss = st.session_state

st.set_page_config(
    page_title='Personal Pythagorean Triangle',
    page_icon='🔼',
    layout='wide',)

st.markdown("""
    <style>
    
           /* Remove blank space at top and bottom */ 
           .block-container {
               padding-top: 0rem;
               padding-bottom: 0rem;
            }
           
           /* Remove blank space at the center canvas */ 
           .st-emotion-cache-z5fcl4 {
               position: relative;
               top: -15px;
               }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 10px;
    left: 15px;
    text-align: left;
    font-size: 14px;
    color: #888;
    border: 1px solid #3399ff33;
    padding: 6px 10px;
    border-radius: 8px;
    background-color: #f9f9f955;
    backdrop-filter: blur(6px);
}

.footer a {
    color: #3399ff;
    text-decoration: none;
    font-weight: 500;
}

.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# --- Footer HTML with hyperlink ---
st.markdown(
    '<div class="footer">Made by <a href="https://github.com/LLLaci" target="_blank">LLLaci</a></div>',
    unsafe_allow_html=True
)

if "init" not in ss:
    ss.init = True
    ss.search_word = ""
    ss.number = 0
    ss.exclude_zero = True
    ss.only_relative_primes = True
    ss.factor = 1
    ss.parameters = {"search_word" : {"value" : "", "text" : "Your words"},
                     "number" : {"value" : 0, "text" : "Your words converted to number"},
                     "operations" : {"value": "", "text" : "List of operations"},
                     "factor" : {"value" : 1, "text" : "GCD (Greatest Common Divisor)"},
                     "m" :      {"value" : 1, "text" : "m"},
                     "n" :      {"value" : 0, "text" : "n"},
                     "A" :      {"value" : 0, "text" : "A = GCD × (m² + 2mn)"},
                     "B" :      {"value" : 1, "text" : "B = GCD × (2mn + 2n²)"},
                     "C" :      {"value" : 0, "text" : "C = GCD × (m² + 2mn + 2n²) = GCD × √(A² + B²)"}}

def get_root_and_remainder(number):
    if number < 0:
        return 0,0
    else:
        root = math.isqrt(number)
        remainder = number - root * root
        return root, remainder
    
def desect_number(number, how_many_pieces = 2):
    sqRoot = 0
    remainder = 0
    sqRoot, remainder = get_root_and_remainder(1 + 8 * number)
    layer = int((sqRoot - 1) // 2)
    new_number_1 = number - ((layer * layer + layer) // 2)
    new_number_2 = layer - new_number_1
    if how_many_pieces == 2:
        new_numbers = [new_number_1, new_number_2] 
    else:
        new_numbers = [new_number_1] + desect_number(new_number_2, how_many_pieces - 1)
    return new_numbers 

def join_numbers(list):  #Reverse function of desect_numbers function, not in use
    layer = list[-1] + list[-2] 
    layer_start = int(layer * (layer + 1) // 2)
    unified_number = layer_start + list[-2]
    if len(list) > 2:
        new_list = list[0:-2] + [unified_number]
        unified_number = join_numbers(new_list)
    return unified_number

def iterate_parameters(list_of_operations, starting_ascii_code):
    m0 = 1
    n0 = 0
    if list_of_operations == "":
        pass
    else:
        for operation in list_of_operations:
            if operation == chr(starting_ascii_code + 2):
                m1 = m0 + 2 * n0               
                n1 = m0 + n0
                m0 = m1
                n0 = n1                
            elif operation == chr(starting_ascii_code + 1):
                n1 = m0 + n0
                n0 = n1                
            elif operation == chr(starting_ascii_code + 0):
                m1 = m0 + 2 * n0
                m0 = m1
    ss.parameters["m"]["value"] = m0
    ss.parameters["n"]["value"] = n0
    return m0,n0

def calculate_pythagorean_triple(list_of_operations, starting_ascii_code, factor = 1):
    m,n = iterate_parameters(list_of_operations, starting_ascii_code)
    A = factor * (m * m + 2 * m * n)
    B = factor * (2 * n * n + 2 * m * n)
    C = factor * (m * m + 2 * m * n + 2 * n * n)
    return A,B,C

def calculate_pythagorean_triangle(number, relative_primes = True, zero_cotenus_excluded = True, starting_ascii_code = 88):
    factor = 1
    if (relative_primes == False):
        number, factor = desect_number(number, 2)
        factor = factor + 1
    if (zero_cotenus_excluded == True):
        number = number + 1
    list_of_operations = ""
    ss.parameters["number"]["value"] = number    
    while (number > 0):
        remainder = int(number % 3)
        list_of_operations = chr(88 + remainder) + list_of_operations
        if remainder == 2:
            number = number + 1
        number = int(number // 3)
    ss.parameters["factor"]["value"] = factor
    ss.parameters["operations"]["value"] = list_of_operations    
    A,B,C = calculate_pythagorean_triple(list_of_operations, starting_ascii_code, factor)
    ss.parameters["A"]["value"] = A
    ss.parameters["B"]["value"] = B
    ss.parameters["C"]["value"] = C
    return(A,B,C)

def integer_check(string):
    is_integer = True
    for char in string[1:]:
        if char not in ["0","1","2","3","4","5","6","7","8","9"]:
            is_integer = False
    if len(string) > 1:
        char = string[0]
        if char not in ["0","1","2","3","4","5","6","7","8","9","-"]:
            is_integer = False  
    elif len(string) == 1:
        char = string[0]
        if char not in ["0","1","2","3","4","5","6","7","8","9",]:
            is_integer = False     
    else:
        is_integer = False
    return(is_integer)


def convert_string_to_number(string):
    if integer_check(string) == True:
        number = int(string)
        if number < 0: 
            number = -1 * number
    else:
        number = 0
        for char in string[::-1]:
            number = number * 256 + ord(char)
    return(number)

st.title("Personal Pithagorean Triangle")
st.markdown("Type your name to the text box and get your personal Pythagorean triple.")
container = st.container(border = True)
with container:
    cols = st.columns([10,1])
    with cols[0]:
        ss.search_word = st_keyup("Type your name:", value = ss.search_word, key = "input_box")
    cols = st.columns([2,2,5])
    with cols[0]:            
        exclude_zero = ss.exclude_zero
        exclude_zero = st.checkbox(label = "Exclude zero length as cotenus", value = ss.exclude_zero)
        if exclude_zero != ss.exclude_zero:
            ss.exclude_zero = exclude_zero
            st.rerun()
    with cols[1]:
        only_relative_primes = ss.only_relative_primes            
        only_relative_primes = st.checkbox(label = "Only consider relative prime triplets", value = ss.only_relative_primes)
        if only_relative_primes != ss.only_relative_primes:
            ss.only_relative_primes = only_relative_primes
            st.rerun()
    ss.parameters["search_word"]["value"] = ss.search_word
    ss.number = convert_string_to_number(ss.search_word)
    calculate_pythagorean_triangle(ss.number, ss.only_relative_primes, ss.exclude_zero)            
    with st.expander("Show parameters"):
        for key,value in ss.parameters.items():
            cols = st.columns([2,7])
            with cols[0]:
                st.write(ss.parameters[key]["text"])
            with cols[1]:
                st.write(str(ss.parameters[key]["value"])) 
    st.markdown("""Your Personal Pythagorean Triplet:  
                A² + B² = C²""")               
    if (ss.parameters["search_word"]["value"]  != ""):
        st.write("")
        for i in range(0,3):
            letter = chr(65 + i)
            st.write(f"{letter} = {ss.parameters[letter]["value"]}")
    else:
        st.write("Please start typing.")
    with st.expander("How does it work?"):
        st.markdown("""
        All primitive Pythagorean triples can be generated using the following formula:

        **A** = *m² + 2mn*  
        **B** = *2mn + 2n²*  
        **C** = √(A² + B²) = *m² + 2mn + 2n²*

        To generate a primitive Pythagorean triple with this formula, *m* must be odd and coprime to *n*. This formula is a modification of [Euclid's formula](https://en.wikipedia.org/wiki/Pythagorean_triple#Generating_a_triple) for generating Pythagorean triples.

        This modification ensures that every positive pair *(m, n)* produces positive values for **A**, **B**, and **C**.

        From each pair *(m, n)*, three new pairs can be generated by changing the signs of the triple's members.
        """)
        with st.expander("Example"):
            st.markdown("""
                Starting values:

                *m* = 1  
                *n* = 1

                **A** = *m² + 2mn* = 1² + 2×1×1 = **3**  
                **B** = *2mn + 2n²* = 2×1×1 + 2×1² = **4**  
                **C** = √(A² + B²) = *m² + 2mn + 2n²* = 1² + 2×1×1 + 2×1² = **5**

                From this initial triple, we can generate three new primitive triples and their corresponding *(m, n)* pairs using the following method:

                **First case:**

                **A** = -3  
                **B** = 4  
                **C** = 5

                We can calculate the new values of *m* and *n*:

                *m* = √(C - B) = 1  
                *n* = √((C - A) / 2) = 2

                **A** = *m² + 2mn* = 1² + 2×1×2 = **5**  
                **B** = *2mn + 2n²* = 2×1×2 + 2×2² = **12**  
                **C** = √(A² + B²) = *m² + 2mn + 2n²* = 1² + 2×1×2 + 2×2² = **13**

                **Second case:**

                **A** = 3  
                **B** = -4  
                **C** = 5

                We can calculate the new values of *m* and *n*:

                *m* = √(C - B) = 3  
                *n* = √((C - A) / 2) = 1

                **A** = *m² + 2mn* = 3² + 2×3×1 = **15**  
                **B** = *2mn + 2n²* = 2×3×1 + 2×1² = **8**  
                **C** = √(A² + B²) = *m² + 2mn + 2n²* = 3² + 2×3×1 + 2×1² = **17**

                **Third case:**

                **A** = -3  
                **B** = -4  
                **C** = 5

                We can calculate the new values of *m* and *n*:

                *m* = √(C - B) = 3  
                *n* = √((C - A) / 2) = 2

                **A** = *m² + 2mn* = 3² + 2×3×2 = **21**  
                **B** = *2mn + 2n²* = 2×3×2 + 2×2² = **20**  
                **C** = √(A² + B²) = *m² + 2mn + 2n²* = 3² + 2×3×2 + 2×2² = **29**
                """)
        st.markdown("""
        Each generated triple can in turn serve as the starting point for three new primitive Pythagorean triples.
        """)

        with st.expander("Generic form"):
            st.markdown("""
            **First case:**

            **m₁** = *m₀*  
            **n₁** = *m₀ + n₀*

            **Second case:**

            **m₁** = *m₀ + 2n₀*  
            **n₁** = *n₀*

            **Third case:**

            **m₁** = *m₀ + 2n₀*  
            **n₁** = *m₀ + n₀*
            """)       

        st.markdown("""
        Using this approach, it is possible to reconstruct [Berggrens's tree of primitive Pythagorean triples](https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples).

        For any given number, a sequence of the three operations can be obtained by converting the number to base 3.

        The only remaining step is to convert your name into a number. This can be done easily by using the ASCII values of its characters.
        """)


        



