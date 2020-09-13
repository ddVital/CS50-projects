document.addEventListener('DOMContentLoaded', function() {

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
	document.querySelector('#compose').addEventListener('click', compose_email);

	// By default, load the inbox
	load_mailbox('inbox');
});

// send mail
document.addEventListener("DOMContentLoaded",function () {
    const form = document.querySelector("#compose-form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        receiver = document.querySelector("#compose-recipients");
        subject = document.querySelector("#compose-subject");
        body = document.querySelector("#compose-body");
        fetch(`/emails`, {
            method: "POST",
            body: JSON.stringify({
                recipients: receiver.value,
                subject: subject.value,
                body: body.value,
            }),
        })
		load_mailbox('sent');
    })
})

function compose_email() {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#view-specific-email').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'block';

	// Clear out composition fields
	document.querySelector('#compose-recipients').value = '';
	document.querySelector('#compose-subject').value = '';
	document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
	
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#view-specific-email').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';

	// Show the mailbox name
	document.querySelector('#emails-view').innerHTML = `<h3>
		${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}
	</h3>`;
	
	// display emails
	fetch(`/emails/${mailbox}`)
	.then(response => response.json())
	.then(emails => {
		emails.forEach(email => {
			if (mailbox == 'inbox' || mailbox == 'sent' || mailbox == 'archive') {
				showEmails(email);
			}
		});
	});
}

function showEmails(email) {
	// create the emails' div
	const element = document.createElement('div');
	element.id = "mail-inbox";
	element.innerHTML = `
	<span id="sender" title="${email.read}">${email.sender}</span>
	<span id="subject">${email.subject}</span>
	<span id="timestamp">${email.timestamp}</span>
	`;

	// veryfi if is read and then change the class
	if (email.read === false) element.className = 'unread';
	else element.className = 'read';

	document.querySelector('#emails-view').append(element);

	element.addEventListener('click', view => {
		viewEmail(email.id);
	});
}

// Display a specific email
function viewEmail(id) {
	document.querySelector('#view-specific-email').innerHTML = '';  //Clears any data from previously opened emails
	const item = document.createElement('div');
	item.id = "view-mail";
	
	fetch(`/emails/${id}`)
	.then(response => response.json())
	.then(email => {
		item.innerHTML = `
			<p><strong>From</strong>: ${email.sender}</p>
			<p><strong>To</strong>: ${email.recipients}</p>
			<p><strong>Subject</strong>: ${email.subject}</p>
			<p><strong>Timestamp</strong>: ${email.timestamp}</p>
			<button class="btn btn-sm btn-outline-primary" id="archive" onclick="archive(${email.id}, ${email.archived})">Archive</button>
			<button class="btn btn-sm btn-outline-primary" id="reply" onclick="reply('${email.id}')">Reply</button>
			<hr>
			<p>${email.body}</p>
		`;

		// verify if email was send by the user
		fetch('emails/sent')
		.then(response => response.json())
		.then(mails => {
			let mailsSent = Array() 
			mails.forEach(mail => {
				mailsSent.push(mail.id);
			})

			// if sent dont display archive button
			if (mailsSent.includes(email.id)) {
				document.querySelector('#archive').style.display = 'none';
			}
		});
		
		markRead(email.id);
		
		if (email.archived == true) {
			document.querySelector('#archive').innerText = 'Unarchive'; 
		}
	});	
	
	document.querySelector('#view-specific-email').appendChild(item);
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#view-specific-email').style.display = 'block';
}

function reply(id) {
	compose_email()
	fetch(`/emails/${id}`)
	.then(response => response.json())
	.then(email => {
		document.querySelector('#compose-recipients').value = email.sender;
		IsReplyed = "Re: ".includes(email.subject);
		if (IsReplyed) {
			document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
		} else {
			document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
			document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote: \n"${email.body}"`;
		}
	});
}

function markRead(id) {
	fetch(`/emails/${id}`, {
		method: 'PUT',
		body: JSON.stringify({
			read: true
		})
	})
}

function archive(id, value) {
	fetch(`/emails/${id}`, {
		method: 'PUT',
		body: JSON.stringify({
			archived: !value
		})
	})

	load_mailbox('inbox')
}