import * as core from '@angular/core';
import { HttpClient, HttpEventType, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { timeout } from 'rxjs/operators';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, FormControl, Validators, AbstractControl } from '@angular/forms';
import { fabric } from 'fabric';

const httpOptions = {
  headers: new HttpHeaders({ 
    'Access-Control-Allow-Origin':'*',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'
  })
};

@core.Component({
  selector: 'app-input-video',
  templateUrl: './input-video.component.html',
  styleUrls: ['./input-video.component.css']
})

export class InputVideoComponent implements core.OnInit {
  uploadedFiles: Array<File>;
  @core.Input() state: boolean;
  processingStatus = false;
  @core.Output() stateOff = new core.EventEmitter();
  uploadStatus = 0;
  scalingFactorX = 1;
  scalingFactorY = 1;
  uploaded = false;
  @core.ViewChild('inputSpeed', { static: true }) inputSpeed: any;

  imageToShow: any;
  isImageLoading: any;
  fileName = '';
  uploadDisabled = false;
  fileSize = 0;
  inputSpeedForm: FormGroup;
  roadLengthForm: FormGroup;
  speedLimit: number;
  roadLength: number;
  canvas: any;
  polygonPoints = [];
  lines = [];
  isDrawing = false;
  mouseDownCounter = 0;
  startPoint: any;
  lane = new Array();
  pedestrian = new Array();
  zebra = new Array();


  constructor(private http: HttpClient, private modalService: NgbModal, private fb: FormBuilder) {
  }

  ngOnInit() {
    this.inputSpeedForm = this.fb.group({
      speedLimit: new FormControl(null, [Validators.required, Validators.min(10), Validators.max(200)])
    });
    this.roadLengthForm = this.fb.group({
      roadLength: new FormControl(null, [Validators.required, Validators.min(1), Validators.max(200)])
    });
  }
  startProcessing() {
    this.processingStatus = true;
    const videoFileName = this.uploadedFiles[0].name;
    this.isImageLoading = true;
    this.getImage('/api/getframe/' + videoFileName).subscribe(data => {
      console.log(data);
      this.imageToShow = data;
      this.openModal(this.inputSpeed);
    });
  }

  finishProcessing() {
    this.processingStatus = false;
    this.uploadDisabled = false;
    this.stateOff.emit({ state: true });
  }

  fileChange(element) {
    console.log('File change called');
    this.uploadedFiles = element.target.files;
    this.fileName = this.uploadedFiles[0].name;
    this.upload();
  }

  upload() {
    const formData = new FormData();
    this.uploadStatus = 0;
    console.log('Uplad function called');
    this.stateOff.emit({ state: false });
    this.uploadDisabled = true;
    formData.append('video', this.uploadedFiles[0], this.uploadedFiles[0].name);
    this.http.post('/api/postvideo', formData, {
      reportProgress: true,
      observe: 'events',
      headers: new HttpHeaders({ 
        'Access-Control-Allow-Origin':'*',
        'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'
      })
    })
      .subscribe((event) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.uploadStatus = Math.round(event.loaded / event.total * 100);
          console.log('Upload Progress : ' + Math.round(event.loaded / event.total * 100) + '%');
        }
        else if (event.type === HttpEventType.Response) {

          console.log('event received is ', event);
        }
      });

  }

  getImage(imageUrl: string): Observable<Blob> {
    return this.http.get(imageUrl, {
      responseType: 'blob',
        headers: new HttpHeaders({ 
        'Access-Control-Allow-Origin':'*',
        'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'
        })
    });
  }

  openModal(inputSpeed) {
    this.modalService.open(inputSpeed);
  }

  saveSpeed(inputSpeed: { value: number; }, inputZebra: any) {
    this.speedLimit = inputSpeed.value;
    console.log(this.speedLimit);
    this.loadCanvas(inputZebra);
  }

  saveRoadLength(inputRoadLength) {
    console.log('Save road length input val:', inputRoadLength.value);
    this.roadLength = inputRoadLength.value;
    const parameters = new FormData();
    parameters.append('speedL', JSON.stringify(this.speedLimit));
    parameters.append('laneC', JSON.stringify(this.lane));
    parameters.append('pedestrianC', JSON.stringify(this.pedestrian));
    parameters.append('zebraC', JSON.stringify(this.zebra));
    parameters.append('roadL', JSON.stringify(this.roadLength));
    console.log(JSON.stringify(this.zebra));
    this.http.post('/api/postparameters', parameters, httpOptions).pipe(timeout(2147483647))
      .subscribe((response) => {
        this.finishProcessing();
        console.log('response received is ', response);
      });
  }

  loadCanvas(modalName) {
    this.modalService.open(modalName, { size: 'xl' });
    (document.getElementById('btnCC') as HTMLInputElement).disabled = true;
    (document.getElementById('gc') as HTMLInputElement).disabled = true;
    const self = this;

    this.canvas = new fabric.Canvas('canvas', {
      backgroundColor: null,
    });
    this.canvas.hasControls = false;
    const img = new Image();
    img.onload = function() {
      console.log(img);
      self.canvas.setDimensions({
        width: Math.min(700, img.width),
        height: Math.min(500, img.height),
      });
      self.scalingFactorX = 1.0*img.width / self.canvas.width;
      self.scalingFactorY = 1.0*img.height / self.canvas.height;  
      console.log("img widht and height are ",img.width,img.height);
      console.log("canvas width and height are ", self.canvas.width, self.canvas.height);
      self.canvas.setBackgroundImage(img.src, self.canvas.renderAll.bind(self.canvas), {
        originX: 'left',
        originY: 'top',
        left: 0,
        top: 0,
        scaleX: self.canvas.width*1.0 / img.width,
        scaleY: self.canvas.height*1.0 / img.height
      });
    };

    img.onerror = function() {
      alert('Try Again');
    };

    img.src = URL.createObjectURL(this.imageToShow);
    console.log(this.canvas.width, this.canvas.height);

    this.startPoint = new fabric.Point(0, 0);
    this.canvas.on('mouse:down', function(evt) {
      if (self.isDrawing) {
        const mouse = this.getPointer(evt.e);
        const x = mouse.x;
        const y = mouse.y;
        const line = new fabric.Line([x, y, x, y], {
          strokeWidth: 3,
          selectable: false,
          stroke: 'red'
        });
        self.polygonPoints.push(new fabric.Point(x, y));
        self.lines.push(line);
        this.add(line);
        this.selection = false;
        self.mouseDownCounter = self.mouseDownCounter + 1;
        if (self.mouseDownCounter === 4) {
          if (self.isDrawing) {
            self.finalize();
          }
        }
      }
    });

    this.canvas.on('mouse:up', function(evt) {
      if (self.lines.length && self.isDrawing) {
        const mouse = this.getPointer(evt.e);
        self.lines[self.lines.length - 1].set({
          x2: mouse.x,
          y2: mouse.y
        }).setCoords();
        this.renderAll();
      }
    });

    this.canvas.on('mouse:move', function(evt) {
      if (self.lines.length && self.isDrawing) {
        const mouse = this.getPointer(evt.e);
        self.lines[self.lines.length - 1].set({
          x2: mouse.x,
          y2: mouse.y
        }).setCoords();
        this.renderAll();
      }
    });
  }

  btnClick() {
    if (this.isDrawing) {
      this.finalize();
    }
    else {
      this.isDrawing = true;
    }
  }

  finalize() {
    this.isDrawing = false;
    const objects = this.canvas.getObjects('line');
    for (const i in objects) {
      if (true){
        this.canvas.remove(objects[i]);
      }
    }
    this.canvas.add(this.makePolygon()).renderAll();
    this.canvas.selection = true;
    this.lines.length = 0;
    this.polygonPoints.length = 0;
    (document.getElementById('btnCC') as HTMLInputElement).disabled = false;
    (document.getElementById('btnRoof') as HTMLInputElement).disabled = true;
    (document.getElementById('gc') as HTMLInputElement).disabled = false;
  }

  makePolygon() {
    const left = fabric.util.array.min(this.polygonPoints, 'x');
    const top = fabric.util.array.min(this.polygonPoints, 'y');
    this.polygonPoints.push(new fabric.Point(this.polygonPoints[0].x, this.polygonPoints[0].y));
    return new fabric.Polygon(this.polygonPoints.slice(), {
      left,
      top,
      fill: 'rgba(0,0,0,0)',
      stroke: 'red',
      strokeWidth: 3,
      selectable: false,
    });
  }

  clearCanvas() {
    const objects = this.canvas.getObjects('polygon');
    for (const i in objects) {
      if (true){
        this.canvas.remove(objects[i]);
      }
    }
    this.mouseDownCounter = 0;
    this.isDrawing = false;
  }

  diableButtonsOnClearCanvas() {
    (document.getElementById('btnRoof') as HTMLInputElement).disabled = false;
    (document.getElementById('btnCC') as HTMLInputElement).disabled = true;
    (document.getElementById('gc') as HTMLInputElement).disabled = true;
    (document.getElementById('pp') as HTMLInputElement).innerHTML = '';
  }

  getCoordinatesZebra() {
    if (this.mouseDownCounter !== 4) {
      this.clearCanvas();
      alert('Draw only a 4-sided polygon.');
    }
    const objects = this.canvas.getObjects('polygon');
    const ppoints = objects[0].get('points');
    let ptext = '';
    for (let i = 0; i < ppoints.length - 1; i++) {
      ptext = ptext + ppoints[i].x + ',' + ppoints[i].y + ';';
      this.zebra[i] = [this.scalingFactorX * ppoints[i].x, this.scalingFactorY * ppoints[i].y];
      console.log(this.zebra);
    }
  }

  getCoordinatesPedestrian() {
    if (this.mouseDownCounter !== 4) {
      this.clearCanvas();
      alert('Draw only a 4-sided polygon.');
    }
    const objects = this.canvas.getObjects('polygon');
    const ppoints = objects[0].get('points');
    let ptext = '';
    for (let i = 0; i < ppoints.length - 1; i++) {
      ptext = ptext + ppoints[i].x + ',' + ppoints[i].y + ';';
      this.pedestrian[i] = [this.scalingFactorX * ppoints[i].x, this.scalingFactorY * ppoints[i].y];
      console.log(this.pedestrian);
    }
  }

  getCoordinatesLane() {
    if (this.mouseDownCounter !== 4) {
      this.clearCanvas();
      alert('Draw only a 4-sided polygon.');
    }
    const objects = this.canvas.getObjects('polygon');
    const ppoints = objects[0].get('points');
    let ptext = '';
    for (let i = 0; i < ppoints.length - 1; i++) {
      ptext = ptext + ppoints[i].x + ',' + ppoints[i].y + ';';
      this.lane[i] = [this.scalingFactorX * ppoints[i].x, this.scalingFactorY * ppoints[i].y];
      console.log(this.lane);
    }
  }
}
