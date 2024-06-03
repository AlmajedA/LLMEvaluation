import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { Message } from '../models/message.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ChatbotService {
  constructor(private http: HttpClient) {}

  conversation = new BehaviorSubject<Message[]>([]);
  botResponse!: string;

  update(msg: Message) {
    this.conversation.next([msg]);
  }

  converse(msg: string, version: string) {
    const userMessage = new Message(msg, 'user');
    this.update(userMessage);

    this.getResponse(msg, version).subscribe((data) => {
      const botMessage = new Message(data.response, 'bot');
      this.update(botMessage);
    });
  }

  getResponse(message: string, version: string): Observable<any> {
    const url = `${environment.backendUrl}/llm/querygpt${version}/`;
    const body = { query: message };
    return this.http.post(url, body);
  }

  clearConversation() {
    this.conversation.next([]);
  }
}
