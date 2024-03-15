import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
from conectar import conectar

conexao = conectar()
 
# Class MyHandler = Try to open 'login.html' file

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        
        try:
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close
            return None

        except FileNotFoundError:
            pass
 
        return super().list_directory(path)

# GET = Try to open and read 'login.html' file
      
    def do_GET(self):
        if self.path =='/login':

            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          

            except FileNotFoundError:
                pass

# Path if the login or password be incorrect 
                     
        elif self.path == '/login_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 

# Path if the class/activity is already registered
            
        elif self.path == '/turma_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = " Turma já cadastrada. Tente novamente!"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 
        
        elif self.path == '/atividade_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()

            mensagem = " Atividade já cadastrada. Tente novamente!"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 

# New user register 
       
        elif self.path.startswith('/novo_cadastro'):
 

            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login',[''])[0]
            senha = query_params.get('senha',[''])[0]
 
            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui.Complete seu cadastro"
 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'cadastro.html'),'r', encoding='utf-8') as novo_cadastro_file:
                content = novo_cadastro_file.read()
 
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}',welcome_message)
 
            self.wfile.write(content.encode('utf-8'))
 
            return

# open and read 'cadastro_turma.html' file
              
        elif self.path == '/turma':
            self.send_response(200)
            self.send_header("content-type","text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8')) 
        
            

        elif self.path == '/atividade':
            
            self.send_response(200)
            self.send_header("content-type","text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8'))          

        else:

            super().do_GET()

# check if the user already exists 
            
    def usuario_existente(self, login, senha):
        cursor = conexao.cursor()
        cursor.execute("SELECT senha FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            # criptography the password
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
            return senha_hash == resultado[0]
        return False

# check if the class already exists
    
    def turma_existente(self, descricao):
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        return False
    
    def atividade_existente(self, descricao):
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        return False
            

# function to add an user
    
    def adicionar_usuario(self,login,senha,nome):
        cursor = conexao.cursor()
        senha_hash = hashlib.sha256(senha.encode("UTF-8")).hexdigest()
        cursor.execute("INSERT INTO dados_login (login, senha, nome) VALUES (%s, %s,  %s)", (login, senha_hash, nome))
        conexao.commit()
        cursor.close()

# function to add a class
              
    def adicionar_turmas(self, descricao, id_professor):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas (descricao) VALUES (%s)", (descricao,))
        cursor.execute("SELECT id_turma FROM turmas WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.execute("INSERT INTO turmas_professor (id_professor, id_turma) VALUES (%s, %s)", (id_professor, resultado[0],))
        conexao.commit()
        cursor.close()

    def adicionar_atividade(self, descricao, id_turma):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividades (descricao) VALUES (%s)", (descricao,))
        cursor.execute("SELECT id_atividade FROM atividades WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.execute("INSERT INTO atividades_turma (id_turma, id_atividade) VALUES (%s, %s)", (id_turma, resultado[0],))
        conexao.commit()
        cursor.close()
    
    def carrega_turmas_professor(self, login):
        cursor = conexao.cursor()
        cursor.execute("SELECT id_professor, nome FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        id_professor = resultado[0]

        cursor = conexao.cursor()
        cursor.execute("SELECT turmas.id_turma, turmas.descricao FROM turmas_professor INNER JOIN turmas ON turmas_professor.id_turma = turmas.id_turma WHERE turmas_professor.id_professor = %s",(id_professor,))
        turmas = cursor.fetchall()
        cursor.close()

        linhas_tabela = ""
        for turma in turmas:
            id_turma = turma[0]
            descricao_turma = turma[1]
            linha = "<tr><td style='text-align:center'>{}</td></tr>".format(descricao_turma)

            linhas_tabela += linha

        
        with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as cad_turma_file:
            content = cad_turma_file.read()

            content = content.replace('{nome_professor}', resultado[1])
            content = content.replace('{id_professor}', str(id_professor))
            content = content.replace('{login}', str(login))

        content = content.replace('<!-- Tabela com linhas zebradas -->', linhas_tabela)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def carrega_atividades_turma(self, login):
        cursor = conexao.cursor()
        cursor.execute("SELECT id_turma, descricao FROM turmas WHERE descricao = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        id_turma = resultado[0]

        cursor = conexao.cursor()
        cursor.execute("SELECT atividades.id_atividade, atividades.descricao FROM atividades_turma INNER JOIN atividades ON atividades_turma.id_atividade = atividades.id_atividade WHERE atividades_turma.id_turma = %s",(id_turma,))
        atividades = cursor.fetchall()
        cursor.close()

        linhas_tabela = ""
        for atividade in atividades:
            id_atividade = atividade[0]
            descricao_atividade = atividade[1]
            linha = "<tr><td style='text-align:center'>{}</td></tr>".format(descricao_atividade)

            linhas_tabela += linha

        
        with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as cad_atividade_file:
            content = cad_atividade_file.read()

            content = content.replace('{nome_turma}', resultado[1])
            content = content.replace('{id_turma}', str(id_turma))
            content = content.replace('{login}', str(login))

        content = content.replace('<!-- Tabela com linhas zebradas -->', linhas_tabela)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
 
# POST function
                
    def do_POST(self):

        # Rota para enviar o login

        if self.path == '/enviar_login':
 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)

            # Acessa os dados do login
 
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]

        
            if self.usuario_existente(login, senha):
                self.carrega_turmas_professor(login)
                
            else:

                cursor = conexao.cursor()
                cursor.execute("SELECT login FROM dados_login WHERE login = %s", (login,))
                resultado = cursor.fetchone()

                if resultado:

                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    cursor.close()
                    return
               
                else:

                # Adiciona um novo usuário no txt
                    
                    self.send_response(302)
                    self.send_header('Location', f'novo_cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    cursor.close()
                    return
            
        # Lógica quando há novo usuário
 
        elif   self.path.startswith('/confirmar_cadastro'):
            
            content_length = int(self.headers['Content-Length'])
            
            body= self.rfile.read(content_length).decode('utf-8')
            
            from_data = parse_qs(body, keep_blank_values=True)
 
            login = from_data.get('email', [''])[0]
            senha = from_data.get('senha', [''])[0]
            nome = from_data.get('nome', [''])[0]

            self.adicionar_usuario(login, senha, nome)
            
            self.send_response(302)

            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Registro Recebido com Sucesso".encode('utf-8')) 

        elif self.path == '/cad_turma':           
                 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body, keep_blank_values=True)
 
            descricao = form_data.get('descricao', [''])[0]

            id_professor = form_data.get('id_professor', [''])[0]

            login = form_data.get('login', [''])[0]

            if self.turma_existente(descricao):
                self.carrega_turmas_professor(login)
           
            else:
                self.adicionar_turmas(descricao, id_professor)

                self.carrega_turmas_professor(login)

                cursor = conexao.cursor()
                cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (descricao,))
                resultado = cursor.fetchone()

        elif self.path == '/cad_atividade':           
                 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')

            form_data = parse_qs(body, keep_blank_values=True)

            descricao = form_data.get('descricao', [''])[0]

            id_turma = form_data.get('id_turma', [''])[0]

            login = form_data.get('login', [''])[0]

            if self.atividade_existente(descricao):

                self.carrega_atividades_turma(login)
           
            else:

                self.adicionar_atividade(descricao, id_turma)

                self.carrega_atividades_turma(login)

                cursor = conexao.cursor()
                cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s", (descricao,))
                resultado = cursor.fetchone()

               
        else:
            super(MyHandler,self).do_POST()

# Criação do Servidor

endereco_ip = "0.0.0.0"
porta = 8000
 

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()
 