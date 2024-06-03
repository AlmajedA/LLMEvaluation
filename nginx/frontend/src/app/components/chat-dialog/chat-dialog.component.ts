import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { DomSanitizer, SafeHtml } from '@angular/platform-browser'; // Import DomSanitizer
import { ChatbotService } from '../../services/chatbot.service';

@Component({
  selector: 'app-chat-dialog',
  standalone: true,
  templateUrl: './chat-dialog.component.html',
  styleUrls: ['./chat-dialog.component.scss'],
  imports: [CommonModule, FormsModule],
})
export class ChatDialogComponent {
  @Input() title: string = '';
  @Input() version: string = '';
  @Input() notImplemented: boolean = false; // Add @Input property for not implemented

  messages: { content: string | SafeHtml; type: 'user' | 'bot' }[] = [];
  userInput: string = '';

  constructor(private chatbotService: ChatbotService, private sanitizer: DomSanitizer) {} // Inject DomSanitizer

  sendMessage(): void {
    if (this.notImplemented) {
      return;
    }
    if (this.userInput.trim()) {
      this.messages.push({ content: this.userInput, type: 'user' });
      const userMessage = this.userInput;
      this.userInput = '';

      this.chatbotService.getResponse(userMessage, this.version).subscribe((response) => {
        const sanitizedContent = this.sanitizer.bypassSecurityTrustHtml(response.response);
        const responseWithScore = this.sanitizer.bypassSecurityTrustHtml(
          `${response.response} <p><strong>F1 Score:</strong> ${response.f1_score}</p>`
        );
        this.messages.push({ content: responseWithScore, type: 'bot' });
      });
    }
  }
}
