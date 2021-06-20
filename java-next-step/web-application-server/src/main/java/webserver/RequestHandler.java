package webserver;

import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.net.Socket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RequestHandler extends Thread {
    private static final Logger log = LoggerFactory.getLogger(RequestHandler.class);

    private Socket connection;

    public RequestHandler(Socket connectionSocket) {
        this.connection = connectionSocket;
    }

    public void run() {
        log.debug("New Client Connect! Connected IP : {}, Port : {}", connection.getInetAddress(),
                connection.getPort());

        try (
            InputStream in = connection.getInputStream();
            OutputStream out = connection.getOutputStream()
        ) {
            BufferedReader br = new BufferedReader(new InputStreamReader(in, "UTF-8"));
            String line = br.readLine();
            if (line == null) {
                return;
            }

            log.debug("request line : {}", line);
            String[] tokens = line.split(" ");
            String httpMethod = tokens[0];
            String url = tokens[1];

            String body = "Hello World";

            if(httpMethod.equals("GET")){
              body = handleGet(url);
            }

            while (!line.equals("")) {
                line = br.readLine();
                log.debug("header : {}", line);
            }

            byte[] bodyBytes = body.getBytes();
            DataOutputStream dos = new DataOutputStream(out);

            response200Header(dos, bodyBytes.length);
            responseBody(dos, bodyBytes);
        } catch (IOException e) {
            log.error(e.getMessage());
        }
    }

    private String handleGet(String url) throws IOException {
      if(url.equals("/index.html")){
        return Files.readString(new File("./webapp" + url).toPath());
      }
      return "TODO 404";
    }

    private void response200Header(DataOutputStream dos, int lengthOfBodyContent) {
        try {
            dos.writeBytes("HTTP/1.1 200 OK \r\n");
            dos.writeBytes("Content-Type: text/html;charset=utf-8\r\n");
            dos.writeBytes("Content-Length: " + lengthOfBodyContent + "\r\n");
            dos.writeBytes("\r\n");
        } catch (IOException e) {
            log.error(e.getMessage());
        }
    }

    private void responseBody(DataOutputStream dos, byte[] body) {
        try {
            dos.write(body, 0, body.length);
            dos.flush();
        } catch (IOException e) {
            log.error(e.getMessage());
        }
    }
}
