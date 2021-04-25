import discord
from discord.ext import commands
import asyncio
import youtube_dl
import os
import sys
from discord.utils import get
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix = ["Your Prefix Here"])
token = 'Your Token Here'

@bot.event
async def on_ready():
	print("YoutubeDownloader가 시작되었어요!")

@bot.command(pass_context=True)
async def 다운로드(ctx, url: str):
	ydl_opts = {
		'format': 'bestaudio/best',
		'outtmpl': '%(title)s.mp3',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '128',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.cache.remove()
		dictMeta = ydl.extract_info(url, download=True)
		global MusicName
		MusicName = dictMeta["title"]
	embed = discord.Embed(color=0xabcdef, description=f"다운로드를 완료했어요!")
	embed.add_field(name="제목", value=f"{MusicName}", inline=False)
	await ctx.author.send(embed=embed)

@bot.command()
async def 재생(ctx, url: str):
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild=ctx.guild)
	if voice is None:
		if ctx.author.voice and ctx.author.voice.channel:
			channel = ctx.author.voice.channel
			await channel.connect()
			await ctx.send("채널에 들어갔어요!")
			voice = get(bot.voice_clients, guild=ctx.guild)
		else:
			await ctx.send("채널에 연결해주세요!")
	#queue? make a list!
	await ctx.send(f"{ctx.author.mention}, 잠시 기다려주세요!")
	ydl_opts = {
		'format': 'bestaudio/best',
		'outtmpl': '%(title)s.mp3',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '128',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.cache.remove()
		dictMeta = ydl.extract_info(url, download=True)
		iDuration = dictMeta["duration"]
		global MusicName
		MusicName = dictMeta["title"]
	embed = discord.Embed(color=0xabcdef, description=f"{ctx.author.mention}님이 신청하신 곡을 재생할게요!")
	embed.add_field(name="제목", value=f"{MusicName}", inline=False)
	embed.add_field(name="동영상 길이", value=f"{iDuration}초", inline=False)
	await ctx.send(embed=embed)
	voice.play(discord.FFmpegPCMAudio(f'{MusicName}.mp3'))
	#voice.is_playing()

bot.run(token)