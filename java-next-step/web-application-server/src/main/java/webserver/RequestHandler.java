package webserver;

import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.net.Socket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import util.HttpRequestUtils;
import util.Request;

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

            List<String> lines = new ArrayList<String>();

            String line = br.readLine();

            if(line == null){
              return;
            }
            
            lines.add(line);

            while(!line.equals("")){
              line = br.readLine();
              lines.add(line);
            }

            Request req = HttpRequestUtils.parseRequest(lines);

            log.debug("{} {}", req.getMethod(), req.getRequestPath());

            String body = "Hello World";
            if(req.getMethod().equals("GET")){
              body = handleGet(req);
            }

            byte[] bodyBytes = body.getBytes();
            DataOutputStream dos = new DataOutputStream(out);

            response200Header(dos, bodyBytes.length);
            responseBody(dos, bodyBytes);
        } catch (IOException e) {
            log.error(e.getMessage());
        }
    }

    private String handleGet(Request req) throws IOException {
      if(req.getRequestPath().equals("/index.html")){
        return Files.readString(new File("./webapp" + req.getRequestPath()).toPath());
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
