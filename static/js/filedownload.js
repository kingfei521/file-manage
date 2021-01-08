$(document).ready(function () {


			$('[data-toggle="tooltip"]').tooltip();

			// Select/Deselect checkboxes
			var checkbox = $('table tbody input[type="checkbox"]');
			$("#selectAll").click(function () {
				if (this.checked) {
					checkbox.each(function () {
						this.checked = true;
					});
				} else {
					checkbox.each(function () {
						this.checked = false;
					});
				}
			});
			checkbox.click(function () {
				if (!this.checked) {
					$("#selectAll").prop("checked", false);
				}
			});
		})

            var progress = document.getElementById("progress");
            var progress_wrapper = document.getElementById("progress_wrapper");
            var progress_status = document.getElementById("progress_status");

            var upload_btn = document.getElementById("upload_btn");
            var loading_btn = document.getElementById("loading_btn");
            var cancel_btn = document.getElementById("cancel_btn");

            var alert_wrapper = document.getElementById('alert_wrapper')

            var input = document.getElementById('file_input');
            var file_input_label = document.getElementById('file_input_label');

            var data_line = document.getElementById('insert_data')

            function show_alert(message, alert) {
                alert_wrapper.innerHTML =`
                            <div class="alert alert-${alert} alert-dismissible fade show" role="alert" >
                                <span>${message}</span>
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times</span>
                                    </button>
                            </div>
                         `;

            }

            function input_filename() {
                file_input_label.innerText = input.files[0].name;
            }

            function upload(url) {
                if (!input.value) {

                    show_alert("No file selectes", "warning");

                    return;
                }

                var data = new  FormData();

                var request = new XMLHttpRequest();

                request.responseType = 'json';

                alert_wrapper.innerHTML = "";

                input.disabled = true;

                upload_btn.classList.add("d-none");

                loading_btn.classList.remove("d-none");

                cancel_btn.classList.remove('d-none');

                progress_wrapper.classList.remove("d-none")

                var file = input.files[0];

                var filename = file.name;

                var filesize = file.size;

                document.cookie = `filesize=${filesize}`;
                data.append('file', file);

                request.upload.addEventListener("progress", function (e) {
                    var loaded = e.loaded;
                    var total = e.total;

                    var percentage_complete = (loaded / total) * 100;

                    progress.setAttribute("style", `width: ${Math.floor(percentage_complete)}%`);
                    progress_status.innerText = `${Math.floor(percentage_complete)}% uploaded`;
                })


                request.addEventListener('load', function (e) {

                    if (request.status == 200) {
                        show_alert(`${request.response.message}`, "success");
                        data_line.innerHTML = `
                                <tr>
                                    <td>
                                        <span class="custom-checkbox">
                                        <input type="checkbox" id="checkbox1" name="options[]" value="1">
                                        <label for="checkbox1"></label>
                                        </span>
                                    </td>
                                    <td>${request.response.fize_msg[0]}</td>
                                    <td>${request.response.fize_msg[1]}</td>
                                    <td>${request.response.fize_msg[2]}</td>
                                    <td>${request.response.fize_msg[3]}</td>
                                    <td>
                                        <a href="#DownloadModal" class="edit" data-toggle="modal"><i class="fas fa-cloud-download-alt fa-1x" data-toggle="tooltip" title="Down"></i></a>
                                        <a href="#DeleteModal" class="delete" data-toggle="modal"><i class="fas fa-trash-alt fa-1x" data-toggle="tooltip" title="Delete"></i></a>
                                    </td>
                                </tr>
                        `
                        console.log(request.response)

                    }
                    else {
                        show_alert(`Error uploading file`, "danger");
                    }

                    reset();
                })

                request.addEventListener('error', function (e) {
                    reset();
                    show_alert(`Error uploading file`, "danger");
                })

                request.addEventListener('abort', function (e) {
                    reset();
                    show_alert(`Upload cancelled`, "primary");
                })

                request.open('post', url);
                request.send(data);

                cancel_btn.addEventListener('click', function() {
                    request.abort();
                })
            } // end

            function reset() {
                input.value = null;
                input.disabled = false;
                cancel_btn.classList.add("d-none");
                loading_btn.classList.add("d-none");
                upload_btn.classList.remove("d-none");
                progress_wrapper.classList.add("d-none");
                progress.setAttribute("style", "width: 0%");
                file_input_label.innerText = "Select File";
            }
