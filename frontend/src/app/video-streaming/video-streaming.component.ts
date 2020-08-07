import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-video-streaming',
  templateUrl: './video-streaming.component.html',
  styleUrls: ['./video-streaming.component.css']
})
export class VideoStreamingComponent implements OnInit {
  videoelement: HTMLVideoElement;
  base = '/api/getvideo/';
  url = this.base + 'default';
  @Input() state: boolean;
  constructor() { }

  ngOnInit(): void {
    this.videoelement = document.getElementById('videoPlayer') as HTMLVideoElement;
  }

  reload(feature){
    console.log('Reload in video streaming called with ' + feature);
    console.log('state is ', this.state);
    this.url = this.base + feature;
    this.videoelement = document.getElementById('videoPlayer') as HTMLVideoElement;
    this.videoelement.load();
  }
}
