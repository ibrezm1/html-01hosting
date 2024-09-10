// stream.service.ts
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class StreamService {
  stream_url = 'http://localhost:5000' +  '/stream-content';
  //stream_url = 'http://localhost:5001/stream-gemini';
  streamMessage(message: string,model: string): Observable<string> {

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return new Observable(observer => {
      fetch(this.stream_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, model: model})
      })
      .then(response => response.body!.getReader())
      .then(reader => {
        const decoder = new TextDecoder();
        let output = '';

        const readStream = () => {
          reader.read().then(({ done, value }) => {
            if (done) {
              observer.complete();
              return;
            }
            output += decoder.decode(value);
            observer.next(output);
            readStream();
          });
        };

        readStream();
      })
      .catch(error => observer.error(error));
    });
  }
}