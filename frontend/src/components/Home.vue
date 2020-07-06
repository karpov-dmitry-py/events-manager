<template>
  <div>
    <h2>{{ status }}</h2>
    <button :disabled="!prevPage" @click="fetchEvents(prevPage)">Previous</button>
    <button :disabled="!nextPage" @click="fetchEvents(nextPage)">Next</button>
    <div class='top'></div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Event type</th>
          <th>Start date</th>
          <th>Body</th>
          <th>Author</th>
          <th>edit</th>
          <th>delete</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for='event in events' :key=event.id>
          <td>{{ event.id }}</td>
          <td>{{ event.title }}</td>
          <td>{{ event.event_type }}</td>
          <td>{{ event.start_date }}</td>
          <td>{{ event.body }}</td>
          <td>{{ event.owner }}</td>
          <td><button @click='editEvent(event)'>edit</button></td>
          <td><button @click='deleteEvent(event)'>delete</button></td>
        </tr>
      </tbody>
    </table>
    <br><br><br>
    <form>
      <input size=130 placeholder='title' v-model='currentEvent.title'><br><br>
      <p><select size=4 placeholder='event type' v-model='currentEvent.event_type'>
      <option disabled>event type</option>
      <option value='call' selected>call</option>
      <option value='meeting'>meeting</option>
      <option value='webcast'>webcast</option>
      </select></p>
      <input placeholder='start date' type=datetime-local v-model='currentEvent.start_date'><br><br>
      <textarea cols='130' rows='8' placeholder='body' v-model='currentEvent.body'></textarea><br><br>
      <button @click="addEvent()">Add an event</button>
      <button @click="updateEvent(currentEvent)">Update an event</button>
    </form>

  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  data () {
    return {
      status: '',
      events: [],
      currentEvent: {},
      api_url: 'http://127.0.0.1:8000/api/events/',
      nextPage: null,
      prevPage: null
    }
  },

  async created () {
    await this.fetchEvents()
  },

  methods: {
    async setStatus (response, expectedStatus) {
      const { status } = response
      if (status !== expectedStatus) {
        this.status = `HTTP status: ${status}: ` + JSON.stringify(await response.json())
      } else {
        this.status = ''
      }
    },
    async fetchEvents (url = this.api_url) {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          Authorization: 'Token d38de5854590cd00564e4b0bf4a4b40ec981d336'
        }
      })
      const { results, next, previous } = await response.json()
      this.events = results
      this.nextPage = next
      this.prevPage = previous
      this.setStatus(response, 200)
    },
    async addEvent () {
      const response = await fetch(this.api_url, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Token d38de5854590cd00564e4b0bf4a4b40ec981d336'
        },
        body: JSON.stringify(this.currentEvent)
      })
      await this.fetchEvents()
      this.setStatus(response, 201)
    },
    async deleteEvent (event) {
      const { id } = event
      const response = await fetch(`${this.api_url}${id}/`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Token d38de5854590cd00564e4b0bf4a4b40ec981d336'
        }
      })
      await this.fetchEvents()
      this.setStatus(response, 204)
    },
    async editEvent (event) {
      this.currentEvent = event
    },
    async updateEvent (event) {
      const { id } = event
      const response = await fetch(`${this.api_url}${id}/`, {
        method: 'PUT',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Token d38de5854590cd00564e4b0bf4a4b40ec981d336'
        },
        body: JSON.stringify(this.currentEvent)
      })
      await this.fetchEvents()
      this.setStatus(response, 200)
    }
  }
}
</script>

<style scoped>
form {
         width: 1250px;
         padding: 20px;
         border-radius: 10px;
         box-shadow: 0 4px 16px #ccc;
         font-family: sans-serif;
         letter-spacing: 1px;
}
td, th{
  padding: 3px 20px;
  margin: 0 10px;
  text-align: left;
}

th {
  background: lightblue;
}

button {
  padding: 3px 10px;
  margin: 0 5px;
}

h2 {
  color: red;
}

.top{
  padding: 20px;
}
</style>
