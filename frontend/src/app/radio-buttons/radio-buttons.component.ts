import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-radio-buttons',
  templateUrl: './radio-buttons.component.html',
  styleUrls: ['./radio-buttons.component.css']
})
export class RadioButtonsComponent implements OnInit {

  @Input() state: boolean;
  feature = 'default';
  postUrl = '/api/postfeature';
  @Output() refreshEvent = new EventEmitter();
  constructor(private http: HttpClient) {

  }

  ngOnInit(): void {
    }

  handleClick(event) {
      console.log('Old radio button value: ' + this.feature);
      console.log('New radio button value: ' + event.target.value);
      if (event.target.value !== this.feature){
        this.feature = event.target.value;
        this.refreshEvent.emit({ feature : event.target.value });
      }
  }
}
