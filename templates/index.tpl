{% with "People" as page %}
{% include "header.html" %}
{% endwith %}

<h2>People</h2>

{% if peopleList %}
    <table id="peopleTable">
        <tr class="topRow">
            <td>Photo</td>
            <td>Name</td>
            <td>Status</td>
            <td>Research</td>
            <td>Website</td>
        </tr>
    {% for person in peopleList %}
        <tr style="background-color: {{person.color}}">
            <td><img src="{{ person.photoURL }}" style="height: 100px" /></td>
            <td style="white-space: nowrap">
<script type="text/javascript" language="javascript">
<!--
{
document.write( '<a href="m' + 'a' + 'ilto:' + '{{ person.email|safe }}' + '">' )
}
//-->
</script>{{ person.name }}</a></td>
            <td>{{ person.status }}</td>
            <td>{{ person.research }}</td>
            <td><a href="{{ person.website }}">{{ person.website }}</a></td>
        </tr>
    {% endfor %}
    </table>
{% endif %}

{% include "footer.html" %}
