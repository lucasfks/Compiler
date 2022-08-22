import regex
import sys

PATTERNS_AND_RESPECTIVE_CODE = {
    r"programa": "#include <stdio.h>\n\nvoid main(void) {\n",
    r"fimprog.": "return 0;\n}\n",
    r"^\s*\}\s*$": "}\n",
    r'^\s*\{\s*$': '{\n',
    r'(?<=escreva\s*\(\").*(?=\"\)\s*\.)': ['printf("', '', '");\n'],
    r'(?<=escreva\s*\().*(?=\)\s*\.)': ['printf_with_var', 'printf(', '', ');\n'],
    r'(?<=leia\s*\().+(?=\)\s*\.)': ['scanf(', '', ');\n'],
    r'(?<=se\s+\().+(?=\)\s*entao\s*\{)': ['if (', '', ') {\n'],
    r'(?<=se\s+\().+(?=\)\s*entao\s*$)': ['if (', '', ')\n'],
    r'^\s*senao\s*\{': "else {\n",
    r'^\s*senao\s*$': "else\n",
    r'(?<=enquanto\s\().+(?=\)\s*\{)': ['while (', '', ') {\n'],
    r'(?<=enquanto\s\().+(?=\)\s*$)': ['while (', '', ')\n'],
    r'(?<=declare\s+int\s+).+(?=\s*\.)': ("int", "int ", ";\n"),
    r'(?<=declare\s+float\s+).+(?=\s*\.)': ("float", "float ", ";\n"),
    r'(?<=declare\s+string\s+).+(?=\s*\.)': ("string", "char ", "[2000];\n"),
    r'[\s\p{L}\d\_]+\:\=[\p{L}\d\s\+\-\*\/\(\)\_\.]+': 'expression'
}

def help():
    print(
        """
        Compilador IsiLanguage to C:
        Help: --help
        Como executar o compilador:
            Mac/Linux: python compilador.py <nome_do_arquivo>.isi
            Windows:   py compilador <nome_do_arquivo>.isi
        """
    )

def main():
    
    variables = {
        "int": [],
        "float": [],
        "string": []
    }
    variable_values = {
        # variable_name : variable_value
    }

    if len(sys.argv) == 1 or len(sys.argv) > 2:
        help()
        return
    elif sys.argv[1] == "--help":
        help()
        return
    else:
        filename = sys.argv[1]


    file = open(filename, "r")
    source_code = file.read()

    source_code_lines = source_code.split("\n")

    # Opens C-compiled file to clean its content if it already exists:
    compiled_filename = filename.replace(".isi", ".c")
    with open(compiled_filename, "w") as compiled_file:
        pass

    # Now reopens compilation file in append mode to add lines of code:
    compiled_code = ""
    with open(compiled_filename, "a") as compiled_file:

        for line in source_code_lines:

            if line == "":
                compiled_file.write("\n")


            else:
                for pattern in PATTERNS_AND_RESPECTIVE_CODE:
                    match = regex.search(pattern, line)

                    if match:   # se encontrou um padrão sintático
                        dictionary_value = PATTERNS_AND_RESPECTIVE_CODE[pattern]

                        # Código compilado em formato de lista significa
                        # que é input/output, ou se/entao, ou enquanto:
                        if type(dictionary_value) == list:
                            # Se é input (scanf)
                            if dictionary_value[0].startswith('scanf'):
                                var_name = match.group().strip()

                                # se a variável for do tipo int
                                if var_name in variables['int']:
                                    dictionary_value[1] = f'"%d", &{var_name}'
                                    variable_values[var_name] = 'input'
                                # se a variável for do tipo float
                                elif var_name in variables['float']:
                                    dictionary_value[1] = f'"%f", &{var_name}'
                                    variable_values[var_name] = 'input'
                                # se a variável for do tipo string
                                elif var_name in variables['string']:
                                    dictionary_value[1] = f'"%s", &{var_name}'
                                    variable_values[var_name] = 'input'
                                else:
                                    print(f"---Erro: Variavel {var_name} nao foi declarada.")
                                    return

                                for text in dictionary_value:
                                    compiled_code += text

                            # se é output (printf) de variável
                            elif dictionary_value[0] == ('printf_with_var'):
                                var_name = match.group().strip()

                                # se a variável for do tipo int
                                if var_name in variables['int']:
                                    dictionary_value[2] = f'"%d", {var_name}'
                                # se a variável for do tipo float
                                elif var_name in variables['float']:
                                    dictionary_value[2] = f'"%f", {var_name}'
                                # se a variável for do tipo string
                                elif var_name in variables['string']:
                                    dictionary_value[2] = f'"%s", {var_name}'
                                else:
                                    print(f"---Erro: Variavel {var_name} nao foi declarada.")
                                    return

                                for text in dictionary_value[1:]:
                                    compiled_code += text


                            # Se a tradução está em formato de lista e não é input, 
                            # substituir o segundo elemento (elemento intermediário)
                            # pelo conteúdo do match.
                            else:
                                dictionary_value[1] = match.group()
                                for text in dictionary_value:
                                    compiled_code += text
                        
                        # Código compilado em formato de tupla significa
                        # que é declaração de variável, e o primeiro elemento
                        # da tupla é o tipo da(s) variável(eis).
                        elif type(dictionary_value) == tuple:

                            # Salvar variáveis declaradas no dicionário de variáveis.
                            vars = match.group().strip(" ").split(",")
                            for v in vars:
                                v = v.strip(" ")
                                variables[dictionary_value[0]].append(v)

                            # Se for int:
                            if dictionary_value[0] == "int" or dictionary_value[0] == "float":
                                compiled_code += dictionary_value[1]
                                compiled_code += match.group()
                                compiled_code += dictionary_value[2]

                            # Se for string:
                            elif dictionary_value[0] == "string":
                                for v in vars:
                                    v = v.strip(" ")
                                    compiled_code += dictionary_value[1]
                                    compiled_code += v
                                    compiled_code += dictionary_value[2]

                            # pdb.set_trace()


                        elif dictionary_value == 'expression':
                            # separa operação entre lados direito e esquerdo do sinal de igual (=)
                            sides_of_assignment = match.group().split(":=")

                            # remove espaços
                            sides_of_assignment = [regex.sub("\s+", "", x) for x in sides_of_assignment] 

                            # remove o ponto (.) ao final da operação
                            if sides_of_assignment[-1][-1] == '.':
                                sides_of_assignment[-1] = sides_of_assignment[-1][0:-1]
                                expression_to_be_compiled = sides_of_assignment[0] + " = " + sides_of_assignment[1]
                            else:
                                print(f"---Erro de Compilação---\n->{line}\n   ^ Sintaxe Inválida")
                                print("Falta o ponto (.) ao final da expressao.\n")
                                return

                            # Armazena valor da variavel no dicionário variable_values
                            variable_values[sides_of_assignment[0]] = sides_of_assignment[1]

                            # Separa variáveis e valores do lado direito do sinal de igual (=)
                            sides_of_assignment[1] = regex.sub(r"[\+\-\*\/\(\)]", " ", sides_of_assignment[1])
                            sides_of_assignment[1] = sides_of_assignment[1].split()

                            vars_type = "None"
                            if sides_of_assignment[0] in variables['int']:
                                vars_type = "int"
                            elif sides_of_assignment[0] in variables['float']:
                                vars_type = "float"
                            elif sides_of_assignment[0] in variables['string']:
                                vars_type = "string"
                            else:
                                print(f"---Erro: Variavel {sides_of_assignment[0]} nao foi declarada.")
                                return

                            
                            for e in sides_of_assignment[1]:
                                # remove numeros da lista, só deixando as variáveis
                                if regex.search("^[\d\.]+$", e):
                                    sides_of_assignment[1].remove(e)
                                else:
                                    # verifica se variável foi declarada
                                    if not e in variables[vars_type]:
                                        print(f"---Erro: Tentou atribuir a {sides_of_assignment[0]} um valor do tipo errado, ou usou variável não declarada.")
                                        return

                            # Se todas as variáveis foram declaradas e são do mesmo tipo
                            expression_to_be_compiled = expression_to_be_compiled + ";"
                            compiled_code = expression_to_be_compiled
                            


                        else:
                            compiled_code = dictionary_value

                        compiled_file.write(compiled_code)
                        compiled_code = ""
                        break

                if not match:
                        print(f"---Erro de Compilação---\n->{line}\n   ^ Sintaxe Inválida\n")
                        return

        # Verifica variáveis declaradas não usadas (warning)
        for v in variables["int"]:
            if not v in variable_values:
                print(f"Warning: Variável {v} declarada mas não utilizada.")
        for v in variables["float"]:
            if not v in variable_values:
                print(f"Warning: Variável {v} declarada mas não utilizada.")
        for v in variables["string"]:
            if not v in variable_values:
                print(f"Warning: Variável {v} declarada mas não utilizada.")


    file.close()


if __name__ == "__main__":
    main()
