<template>
  <div>
    <form>
      <input class='filters' placeholder='login' v-model='login'>
      <input class='filters' type='password' placeholder='password' v-model='password'>
      <button @click='doLogin()' :disabled='currentUser'>Login</button>
      <button @click='doLogout()' :disabled='!currentUser'>Logout</button>
      {{ `Current user: ${currentUser}` }}
      <div class='top'></div>
      <button :disabled="!prevPage" @click="fetchEvents(prevPage)">Previous</button>
      <button :disabled="!nextPage" @click="fetchEvents(nextPage)">Next</button>
      <div class='top'></div>
      <div class='filters'>
        <label>Filters:</label>
        <select class='filters' v-model='date_filter'>
          <option value=0 selected>all</option>
          <option value=30>since last 30 days</option>
          <option value=7>since last 7 days</option>
          <option value=1>since yesterday</option>
       </select>
        <input class='filters' placeholder='search by title' v-model='title_filter'>
        <button :disabled="!currentUser" @click="filterEvents()">apply</button>
      </div>
    </form>
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
    <div class='top'></div>
    <form>
      <input size=130 placeholder='title' v-model='currentEvent.title'>
      <p><select size=4 placeholder='event type' v-model='currentEvent.event_type'>
      <option disabled>event type</option>
      <option value='call' selected>call</option>
      <option value='meeting'>meeting</option>
      <option value='webcast'>webcast</option>
      </select></p>
      <input placeholder='start date' type=datetime-local v-model='currentEvent.start_date'><br><br>
      <textarea cols='130' rows='8' placeholder='body' v-model='currentEvent.body'></textarea><br><br>
      <h2 class='status'>{{ status }}</h2>
      <button :disabled="!currentUser" @click="addEvent()">Add an event</button>
      <button :disabled="!currentUser" @click="updateEvent(currentEvent)">Update an event</button>
    </form>

  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  data () {
    return {
      login: '',
      password: '',
      currentUser: null,
      status: '',
      events: [],
      currentEvent: {},
      obtain_token_url: 'http://127.0.0.1:8000/api-token-auth/',
      api_url: 'http://127.0.0.1:8000/api/events/',
      nextPage: null,
      prevPage: null,
      date_filter: 0,
      title_filter: ''
    }
  },

  async created () {
    if (this.currentUser) {
      await this.fetchEvents()
    }
  },

  methods: {
    async doLogin (url = this.obtain_token_url) {
      const credentials = {
        username: this.login,
        password: this.password
      }
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      })
      this.setStatus(response, 200)
      if (response.status === 200) {
        const { token } = await response.json()
        this.currentUser = this.login
        localStorage.setItem(this.login, token)
        await this.fetchEvents()
      }
    },
    doLogout () {
      localStorage.removeItem(this.currentUser)
      this.currentUser = null
      this.events = []
    },
    getAuthToken () {
      const token = localStorage.getItem(this.currentUser)
      return `Token ${token}`
    },
    async setStatus (response, expectedStatus) {
      const { status } = response
      if (status !== expectedStatus) {
        this.status = `Error! HTTP status: ${status}: ` + JSON.stringify(await response.json())
      } else {
        this.status = ''
      }
    },
    async fetchEvents (url = this.api_url) {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          Authorization: this.getAuthToken()
        }
      })
      const { results, next, previous } = await response.json()
      this.events = results
      this.nextPage = next
      this.prevPage = previous
      this.setStatus(response, 200)
    },
    async filterEvents () {
      const url = new URL(this.api_url)
      if (this.date_filter > 0) {
        url.searchParams.set('start_date', this.date_filter)
      }
      this.title_filter = this.title_filter.replace(/\s/g, '')
      if (this.title_filter) {
        url.searchParams.set('title', this.title_filter)
      }
      await this.fetchEvents(url)
    },
    async addEvent () {
      const response = await fetch(this.api_url, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: this.getAuthToken()
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
          Authorization: this.getAuthToken()
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
          Authorization: this.getAuthToken()
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
         width: 1600px;
         padding: 20px;
         border-radius: 10px;
         box-shadow: 0 4px 16px #ccc;
         font-family: sans-serif;
         letter-spacing: 1px;
}

select {
  width: 200px;
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

.status {
  color: red;
}

.top{
  padding: 10px;
}

.filters {
  align: left;
  padding: 3px 5px;
  margin: 10px 5px;
}

</style>
