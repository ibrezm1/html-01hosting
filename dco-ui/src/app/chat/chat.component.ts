import { Component } from '@angular/core';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  message: string = '';
  chatMessages: { user: string; message: string; type: string }[] = [
    { user: 'User', message: 'Explain quantum computing in simple terms', type: 'user' },
    {
      user: 'AI',
      message: 'Quantum computing is a new type of computing that relies on the principles of quantum physics...',
      type: 'ai'
    }
  ];

  sendMessage() {
    if (this.message.trim()) {
      this.chatMessages.push({ user: 'User', message: this.message, type: 'user' });
      this.message = ''; // Clear the input field
      // You can add further logic to send this message to a backend or AI service
    }
  }
}