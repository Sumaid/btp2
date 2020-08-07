import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ViewChild } from '@angular/core';

import { AppComponent } from './app.component';
import { InputVideoComponent } from './input-video/input-video.component';
import { VideoStreamingComponent } from './video-streaming/video-streaming.component';
import { SnapshotsComponent } from './snapshots/snapshots.component';
import { RadioButtonsComponent } from './radio-buttons/radio-buttons.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    AppComponent,
    InputVideoComponent,
    VideoStreamingComponent,
    SnapshotsComponent,
    RadioButtonsComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
  @ViewChild('renderSnapshots', { static: true }) renderSnapshots: any;
  @ViewChild('videoStream', { static: true }) videoStream: any;

  refreshEvent(event){
    console.log('Main app refresh called with ' + event.feature);
    this.renderSnapshots.reload(event.feature);
    this.videoStream.reload(event.feature);
  }
 }
