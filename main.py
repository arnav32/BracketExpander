from latex_to_img import latex2image
from PIL import Image

# Algebraic Expression Expander

# ------------------------------------------ INSTRUCTIONS ------------------------------------------
# Enter as many brackets as you want, each with as many terms as you want.
# The program will output the expanded version of your brackets
# Ensure that there is a space between each term and each sign.

#   example input:
#     (-x^2 + x - 1)(x - 5)
#   output:
#     -x^3 + 6x^2 - 6x + 5

#   example input:
#     (-3x^2 - 4)(3x^-4 - 5 + x + x^3)(2 + x^-5)
#   output:
#     -6x^{5} - 14x^{3} + 30x^{2} - 8x + 37 - 25x^{-2} + 15x^{-3} - 28x^{-4} + 20x^{-5} - 9x^{-7} - 12x^{-9}

import re

inp_expression = input("Enter expression: ")
# inp_expression = "(-0.5x^-2 + 5x^0.8 - 4)(0.1x - 5.2x^2.2)(-9.8x^2 - 12 + 2x)"

def trailing_zeroes(fl):
    return fl if float(fl) % 1 else int(fl)
    # trailing_zeroes = lambda n: n if n % 1.0 else int(n) # Define lambda function to remove trailing zeroes in the float result if needed


def format_inp(inp_expression):
    # 1) create a list with the inners of each bracket
    inners = [x.replace("(", "").replace(")", "")
              for x in re.findall(r'\(.*?\)', inp_expression)]  # e.g. (x^-2 + 5x - 1)(-x - 5) to ("x^-2 + 5x - 1", "-x - 5")

    # 2) put "+" in front of first term in each bracket if there is nothing there
    for i in range(len(inners)): # for the inside of each bracket
        if inners[i][0] not in ["+", "-"]:
            inners[i] = "+ " + inners[i]

    # 3) for the first term in every bracket, format "-5x^2" to "- 5x^2" etc. when needed
        elif inners[i][0] == "-" and inners[i][0:2] != "- ":
            inners[i] = "- " + inners[i][1:]

    # 4) split the inside of each bracket by spaces
    inners = [x.split(" ") for x in inners]

    # 5) for every x term without a given coefficient, show the coefficient of 1
    # STEP 5) NOT NEEDED DUE TO 'if term0[1][0] != "x" else 1' CHECK WITHIN mult_brackets()
    # for i in range(len(inners)):
    #     for j in range(1, len(inners[i]), 2):
    #         if inners[i][j][0] == "x":
    #             inners[i][j] = "1" + inners[i][j] # inners[i][j][0] is first character of jth term of ith inner

    # 6) pair every term with its sign into a tuple, and do this for each bracket

    paired_brackets = [] # each term is put into a "trio" - that is, a tuple with three elements in the format: (sign coeff, power)
    for inner in inners: # for each bracket
        paired_terms = [] # a list of all terms in a given bracket. each term is given as a trio
        for i in range(0, len(inner), 2): # for each term in each bracket
            sign = inner[i]
            if "x" in inner[i + 1]:
                coeff = float(re.findall(r"(.+?x)", inner[i + 1])[0][:-1]) if inner[i + 1][0] != "x" else 1 # the coefficient of the unsigned term is all chars before x
                power = float(re.findall(r"(?<=\^).*", inner[i + 1])[0]) if "^" in inner[i + 1] else 1 # the power of the unsigned term are any chars after "^", else it is 1
            else:
                coeff = inner[i + 1]
                power = 0 # the power of x in the unsigned term is 0 if there is no x term present
            paired_terms.append((float(f"{sign}{coeff}"), power))
            # paired_terms.append((float(f"{sign}{trailing_zeroes(coeff)}"), trailing_zeroes(power)))
        paired_brackets.append(paired_terms)
    return paired_brackets


def group_like_terms(expression): # Grouping elements using a dictionary
    grouped_terms = {}
    for term_data in expression:
        value = term_data[0]
        key = term_data[1]
        if key in grouped_terms:
            grouped_terms[key].append(value)
        else:
            grouped_terms[key] = [value]

    # # TEST: Printing the grouped data
    # for key, values in grouped_terms.items():
    #     print(key, ":", values)

    grouped_terms = dict(sorted(grouped_terms.items(), reverse=True)) # sort the dictionary by ascending keys
    return grouped_terms


def format_outp(outp_expression):
    formatted = ""
    outp_expression = group_like_terms(outp_expression)
    # Iterate through each key-value pair in the dictionary, concatenating it to the formatted output
    for key in outp_expression:
        sum_coeffs = trailing_zeroes(round(sum(outp_expression[key]), 2))
        if sum_coeffs < 0:
            sum_coeffs = "-" if sum_coeffs == -1 else f"- {str(sum_coeffs)[1:]}"
        elif sum_coeffs > 0:
            sum_coeffs = "" if sum_coeffs == 1 else f"+ {sum_coeffs}"

        if sum_coeffs != 0:
            if key == 0:
                formatted += f"{sum_coeffs} "
            elif key == 1:
                formatted += f"{sum_coeffs}x "
            else:
                formatted += f"{sum_coeffs}x^{{{trailing_zeroes(round(key, 2))}}} " # CHANGE HERE FROM ORIGINAL PROGRAM FOR LATEX FORMATTING (THREE CURLY BRACES VS. ONE IN ORIGINAL)
                # # TEST: Printing the keys with the sum of their stored values
                # print(key)
                # print(sum(outp_expression[key]))

    if formatted[:2] == "- ":
        formatted = formatted[:1] + formatted[2:]
    elif formatted[:2] == "+ ":
        formatted = formatted[2:]
    return formatted.strip()


def mult_brackets(brack0, brack1): # example inputs: [(+6, -2), (+5, 8), (-4, 0)] and [(+1, 1), (-5, 2)]
    output = []
    for term0 in brack0:
        for term1 in brack1:
            output.append((term0[0] * term1[0], term0[1] + term1[1]))
    return output


formatted_inp = format_inp(inp_expression)
formatted_inp_save = formatted_inp.copy()

# Using the associativity law of multiplication to take (a)(b)(c)(d)(e) to (a)(b)(c)(de) to (a)(b)(cde) to (a)(bcde) to (abcde), etc. for any number of brackets
for i in range(len(formatted_inp) - 2, -1, -1):
    formatted_inp[i] = mult_brackets(formatted_inp[i], formatted_inp[i + 1])

unformatted_outp = formatted_inp[0]
formatted_outp = format_outp(unformatted_outp)

# TODO:
#   - Finish mult_brackets() ✔
#   - Write group_like_terms()
#   - Finish format_outp()
#   - Use enumerate() in FOR loops


# ----------------------- TESTS -----------------------
# print(f"input: {inp_expression}")
# print(f"formatted_inp: {formatted_inp_save}")
# print(f"unformatted output: {unformatted_outp}")
print(f"\nExpanded expression: {formatted_outp}")
# (-0.5x^-2 + 5x^8 - 4)(x - 5x^2)(-9x^2 - 12 + 2x)

# latex_expression = r"""$\vec{\nabla}\times\vec{H}=\vec{J}+\dfrac{\partial\vec{D}}{\partial t},$"""
latex_expression = rf"""${formatted_outp}$"""
image_name = "expanded_result.png"
fig = latex2image(latex_expression, image_name, image_size_in=(16, 9), fontsize=20, dpi=700)

img = Image.open("expanded_result.png")

img.show()

# test data: (-0.5x^0.8 - 4)(0.1x - 5.2x^2.2)(-9.8x^2 - 12 + 2x)


# # Trying to crop image to just equation  (using: https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil) (may be helpful also: https://stackoverflow.com/questions/28759253/how-to-crop-the-internal-area-of-a-contour)
# from PIL import Image, ImageChops
#
# def trim(im):
#     bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
#     diff = ImageChops.difference(im, bg)
#     diff = ImageChops.add(diff, diff, 2.0, -100)
#     bbox = diff.getbbox()
#     if bbox:
#         return im.crop(bbox)
#
# img_trim = trim(fig)
# img_trim.show()

