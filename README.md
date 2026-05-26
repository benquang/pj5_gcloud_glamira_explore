<!-- ABOUT THE PROJECT -->
## PJ5 - Glamira exploring Google Cloud

![Product Name Screen Shot][product-screenshot]

Setting up infrastructure and understanding data pipelines with GCP, MongoDB, and Python.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project


## GCP Setup

Overview: create a GCP project, enable billing, and enable the following APIs: Compute Engine, Cloud Storage, and (optionally) Cloud Logging.

### GCS setup

1. Create a GCS bucket for raw and processed data:
	```bash
	gsutil mb -p YOUR_PROJECT -c STANDARD -l YOUR_REGION gs://your-bucket-name
	```
2. Set lifecycle rules or ACLs as needed and upload initial data:
	```bash
	gsutil cp data/* gs://your-bucket-name/raw/
	```

### Vm setup

Use a Bash shell for these commands.

1. Create a VM (Compute Engine) with a public IP or allow SSH via Cloud IAP.
```bash
gcloud compute instances create vm-mongo --zone=YOUR_ZONE --machine-type=e2-medium --image-family=debian-11 --image-project=debian-cloud
```
2. SSH into the VM:
```bash
gcloud compute ssh vm-mongo --zone=YOUR_ZONE
```
3. Install MongoDB (or use a packaged MongoDB on the VM). On Debian/Ubuntu:
```bash
sudo apt update && sudo apt install -y mongodb
```
4. Start and enable MongoDB:
```bash
sudo systemctl enable --now mongodb
```

### MongoDB import data & query

1. Prepare JSON or CSV export files locally or in the VM under /tmp/data/.
2. Import into MongoDB using mongoimport:
```bash
mongoimport --db glamira --collection visits --file /tmp/data/visits.json --jsonArray
```
3. Connect to mongo shell to run queries:
```bash
mongo --eval "db.visits.find().limit(5).pretty()"
```
4. Example queries:
```bash
db.visits.countDocuments({})
db.visits.createIndex({ip:1})
db.visits.aggregate([{ $group: { _id: "$country", count: { $sum: 1 } } }])
```

<!-- USAGE EXAMPLES -->
## Usage

Following steps below

_Folloing steps in this link [Project tasks](https://unigap-tech-coaching.notion.site/Project-05-Data-Collection-Storage-Foundation-fd50b5b264a04576b0def7c0ba1f48af)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Phase 1: Environment Setup (Week 1)
- [x] Phase 2: Storage & Compute Setup (Week 1)
- [x] Phase 3: Data Loading & Exploration (Week 2)
- [x] Phase 4: IP Location Processing (Week 3)
- [x] Phase 5: Product Information Collection (Week 4)
- [ ] Phase 6: Documentation & Testing (Week 4)

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Deliverables

* VM with MongoDB running
* Python scripts for IP processing
* Documentation of data structure
* GitHub repository with organized modules

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: docs/gvto.svg
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
