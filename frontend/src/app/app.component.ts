import { Component, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  state = false;
  @ViewChild('renderSnapshots', { static: true }) renderSnapshots: any;
  @ViewChild('videoStream', { static: true }) videoStream: any;

  refreshEvent(event){
    console.log('Main app refresh called with ' + event.feature);
    this.renderSnapshots.reload(event.feature);
    this.videoStream.reload(event.feature);
  }
  stateOff(event){
    console.log('State off called with ', event.state);
    this.state = event.state;
    if (event.state){
      this.renderSnapshots.reload('default');
      this.videoStream.reload('default');
    }
    console.log('new state is ', this.state);
  }
}
