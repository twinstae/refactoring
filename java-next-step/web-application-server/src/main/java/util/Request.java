package util;

import java.util.Map;

public class Request {
    private String method;
    private String requestPath;
    private Map<String, String> params;
    private Map<String, String> headers;

    public Request(
        String method,
        String requestPath,
        Map<String, String> params,
        Map<String, String> headers
    ){
      this.method = method;
      this.requestPath = requestPath;
      this.params = params;
      this.headers = headers;
    }

    public String getMethod(){ return method; }

    public String getRequestPath(){ return requestPath; }

    public Map<String, String> getParams(){ return params; }

    public Map<String, String> getHeaders(){ return headers; }
}
